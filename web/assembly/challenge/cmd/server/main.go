package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"encoding/binary"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"

	"github.com/sigurn/crc16"
	"github.com/zenazn/pkcs7pad"
)

type QueryHoldingRegisters struct {
	DeviceId         uint8
	FunctionCode     uint8
	StartingRegister uint16
	NumRegisters     uint16
	CRCChecksum      uint16
}

var key = []byte("SecurePassword1!")
var registers = []byte("\x00\x01\x01\x00\x00Hackers were here! Also the flags is: USCG{r1d1ng_th3_bu5_t0_f1ag5}")

func main() {

	http.Handle("/", http.StripPrefix("/", http.FileServer(http.Dir("../../assets"))))
	http.HandleFunc("/api/modbus", handleQuery)

	err := http.ListenAndServe(":1337", nil)
	if err != nil {
		fmt.Println("Failed to start server", err)
		return
	}
}

func handleQuery(w http.ResponseWriter, r *http.Request) {

	var ciphertext, plaintext []byte
	var err error
	var query QueryHoldingRegisters

	bodyBytes, _ := ioutil.ReadAll(r.Body)

	if ciphertext, err = base64.StdEncoding.DecodeString(string(bodyBytes)); err != nil {
		http.Error(w, "Error processing incoming message. Must be valid base-64 encoding.", http.StatusInternalServerError)
		return
	}

	if plaintext, err = decryptCBC(key, ciphertext); err != nil {
		http.Error(w, "Error processing incoming message. Unable to decrypt AES-128-CBC message.", http.StatusInternalServerError)
		return
	}

	if plaintext, err = pkcs7pad.Unpad(plaintext); err != nil {
		http.Error(w, "Error processing incoming message. Unable to decrypt AES-128-CBC message.", http.StatusInternalServerError)
		return
	}

	p := bytes.NewBuffer(plaintext)
	err = binary.Read(p, binary.BigEndian, &query)

	if err != nil {
		http.Error(w, "Error processing incoming message. Must be valid Read Holding Registers query.", http.StatusInternalServerError)
		return
	}

	if query.DeviceId != 1 {
		http.Error(w, "Error processing incoming message. Unknown Modbus Slave ID.", http.StatusInternalServerError)
		return
	}

	if query.FunctionCode != 3 {
		http.Error(w, "Error processing incoming message. Modbus function not implemented.", http.StatusInternalServerError)
		return
	}

	startRegister := int(query.StartingRegister) - 1
	numRegisters := int(query.NumRegisters)
	endRegister := startRegister + numRegisters

	if startRegister < 0 || startRegister > len(registers) {
		http.Error(w, "Error processing incoming message. Starting register out of range.", http.StatusInternalServerError)
		return
	}

	if endRegister < 0 || endRegister > len(registers) {
		http.Error(w, "Error processing incoming message. Ending register out of range.", http.StatusInternalServerError)
		return
	}

	responseBuffer := new(bytes.Buffer)

	var responseData = []any{
		uint8(query.DeviceId),
		uint8(query.FunctionCode),
		uint8(numRegisters * 2),
	}

	for _, v := range responseData {
		err := binary.Write(responseBuffer, binary.BigEndian, v)
		if err != nil {
			http.Error(w, "Internal Error Preparing Response", http.StatusInternalServerError)
			return
		}
	}

	// Write register values
	for _, v := range registers[startRegister:endRegister] {
		err := binary.Write(responseBuffer, binary.BigEndian, uint16(v))
		if err != nil {
			http.Error(w, "Internal Error Preparing Response", http.StatusInternalServerError)
			return
		}
	}

	// Write CRC
	table := crc16.MakeTable(crc16.CRC16_MODBUS)
	crc := crc16.Checksum(responseBuffer.Bytes(), table)

	err = binary.Write(responseBuffer, binary.BigEndian, crc)

	if err != nil {
		http.Error(w, "Internal Error Preparing Response", http.StatusInternalServerError)
		return
	}

	// Encrypt response
	if ciphertext, err = encryptCBC(key, responseBuffer.Bytes()); err != nil {
		fmt.Println(err)
	}

	cleartext := base64.StdEncoding.EncodeToString(ciphertext)

	io.WriteString(w, cleartext)
}

func encryptCBC(key, plaintext []byte) (ciphertext []byte, err error) {

	plaintext = pkcs7pad.Pad(plaintext, aes.BlockSize)

	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}

	ciphertext = make([]byte, aes.BlockSize+len(plaintext))
	iv := ciphertext[:aes.BlockSize]
	if _, err := io.ReadFull(rand.Reader, iv); err != nil {
		panic(err)
	}

	cbc := cipher.NewCBCEncrypter(block, iv)
	cbc.CryptBlocks(ciphertext[aes.BlockSize:], plaintext)

	return
}

func decryptCBC(key, ciphertext []byte) (plaintext []byte, err error) {
	var block cipher.Block

	if block, err = aes.NewCipher(key); err != nil {
		return
	}

	if len(ciphertext) < aes.BlockSize {
		return
	}

	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	cbc := cipher.NewCBCDecrypter(block, iv)
	cbc.CryptBlocks(ciphertext, ciphertext)

	plaintext = ciphertext

	return
}
