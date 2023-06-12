package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"encoding/binary"
	"fmt"
	"io"
	"syscall/js"
	"time"

	"github.com/zenazn/pkcs7pad"
)

var key = []byte("SecurePassword1!")

func main() {

	var ciphertext, plaintext []byte
	var err error

	js.Global().Set("handleResponse", responseWrapper())

	fmt.Println("[INFO] Intializing HMI Interface")
	fmt.Println("[INFO] Modbus Connection Active")

	// Repeat every 30 seconds
	for {

		fmt.Println("[INFO] Querying System...")

		// Query Holding Registers 1-5
		plaintext = []byte("\x01\x03\x00\x01\x00\x05\x09\xd4")

		if ciphertext, err = encryptCBC(key, plaintext); err != nil {
			fmt.Println(err)
		}

		cleartext := base64.StdEncoding.EncodeToString(ciphertext)

		js.Global().Call("hmiRequest", cleartext)

		time.Sleep(30 * time.Second)
	}
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
		fmt.Printf("ciphertext too short")
		return
	}

	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	cbc := cipher.NewCBCDecrypter(block, iv)
	cbc.CryptBlocks(ciphertext, ciphertext)

	plaintext = ciphertext

	return
}

func responseWrapper() js.Func {
	responseFunc := js.FuncOf(func(this js.Value, args []js.Value) any {

		var plaintext, ciphertext []byte
		var err error

		fmt.Println("[INFO] Received Response")

		if len(args) != 1 {
			fmt.Println("[ERROR] Invalid message passed to decryption function.")
			return nil
		}

		inputCiphertext := args[0].String()

		if ciphertext, err = base64.StdEncoding.DecodeString(inputCiphertext); err != nil {
			fmt.Println("[ERROR] Message must be valid base-64.")
			return nil
		}

		if plaintext, err = decryptCBC(key, ciphertext); err != nil {
			fmt.Println("[ERROR] Error decrypting AES-CBC-128 message.")
			return nil
		}

		if plaintext, err = pkcs7pad.Unpad(plaintext); err != nil {
			fmt.Println("[ERROR] Error decrypting AES-CBC-128 message.")
			return nil
		}

		NumBytes := int(plaintext[2])

		idx := 0

		for i := 3; i < 3+NumBytes; i += 2 {
			js.Global().Call("setDeviceStatus", idx, binary.BigEndian.Uint16(plaintext[i:i+2]))
			idx++
		}

		return nil

	})
	return responseFunc
}
