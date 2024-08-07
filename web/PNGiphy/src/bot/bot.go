package bot

import (
	"log"
	"math"
	"os"

	"github.com/tebeka/selenium"
	"github.com/tebeka/selenium/chrome"
)

var appHost = os.Getenv("APP_HOST")
var flag = os.Getenv("FLAG")

func InitChromedriver() {
	_, err := selenium.NewChromeDriverService("./chromedriver", 4444)
	if err != nil {
		log.Fatal("Error:", err)
	}
}

func BotVisit(id string) {
	// Configure the browser options
	caps := selenium.Capabilities{}
	caps.AddChrome(chrome.Capabilities{Args: []string{
		"--headless",
		"--no-sandbox",
		"--disable-dev-shm-usage",
		"--disable-gpu",
		"--disable-extensions",
		"--disable-software-rasterizer",
		"--disable-setuid-sandbox",
		"--ignore-certificate-errors",
		"--media-cache-size=1",
		"--disk-cache-size=1",
	}})

	// create a new remote client with the specified options
	driver, err := selenium.NewRemote(caps, "")
	if err != nil {
		log.Fatal("Error:", err)
	}

	err = driver.Get("http://" + appHost + "/ping")
	if err != nil {
		log.Fatal("Error:", err)
	}

	// Set flag cookie
	err = driver.AddCookie(&selenium.Cookie{
		Name:   "flag",
		Value:  flag,
		Secure: false,
		Expiry: math.MaxUint32,
	})
	if err != nil {
		log.Fatal("Error:", err)
	}

	err = driver.Get("http://" + appHost + "/?image=" + id)
	if err != nil {
		log.Fatal("Error:", err)
	}

	_, err = driver.PageSource()
	if err != nil {
		log.Fatal("Error:", err)
	}

	driver.Quit()
}
