from selenium import webdriver
import time

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datos


# Iniciar el navegador Chrome
driver = webdriver.Chrome()

# Navegar a la URL
driver.get("https://www.demoblaze.com/index.html")


def log_in():
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "#login2").click()

    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "#loginusername").send_keys(datos.userName)
    driver.find_element(By.CSS_SELECTOR, "#loginpassword").send_keys(datos.password)
    driver.find_element(By.XPATH, "//button[contains(text(),'Log in')]").click()

    time.sleep(2)

    name_user = driver.find_element(By.CSS_SELECTOR, "#nameofuser").text
    assert "Welcome " + datos.userName in name_user



def agregar_item(categoria):
    time.sleep(2)

    # Ir a Pagina Principal
    driver.find_element(By.CSS_SELECTOR, "#nava").click()
    time.sleep(2)

    # Seleccionar la categoria //Phones,Laptops,Monitors
    driver.find_element(By.XPATH, categoria).click()
    time.sleep(2)

    # Seleccionar el primer producto
    driver.find_element(By.XPATH, "//body/div[@id='contcont']/div[1]/div[2]/div[1]/div[1]/div[1]/a[1]/img[1]").click()
    time.sleep(2)

    # Se munestra la pagina del producto. Agregar al carrito
    driver.find_element(By.XPATH, "// a[contains(text(), 'Add to cart')]").click()
    time.sleep(2)

    # Se muestra la alerta de producto agregado
    alert = Alert(driver)
    assert alert.text in "Product added."
    alert.accept()



def validar_carrito():
    time.sleep(2)

    # Ir al Carrito
    driver.find_element(By.CSS_SELECTOR, "#cartur").click()
    time.sleep(5)

    # Obtener los valores de la columna
    columna = driver.find_elements(By.XPATH, "//table[@class='table table-bordered table-hover table-striped']/tbody/tr/td[3]")

    # Validar los precios de productos con el Total
    # Iterar sobre la lista de elementos y sumar los valores
    suma = sum([float(elemento.text) for elemento in columna])
    print(suma)

    assert suma == float(driver.find_element(By.CSS_SELECTOR, "#totalp").text)



def checkout():
    time.sleep(2)

    # Ir a Pagina Principal
    driver.find_element(By.CSS_SELECTOR, "#nava").click()
    time.sleep(2)

    # Ir al Carrito
    driver.find_element(By.CSS_SELECTOR, "#cartur").click()
    time.sleep(4)

    # Click en realizar compra
    driver.find_element(By.XPATH, "//button[contains(text(),'Place Order')]").click()
    time.sleep(2)

    # Completar formulario y enviar
    driver.find_element(By.CSS_SELECTOR, "#name").send_keys(datos.name)
    driver.find_element(By.CSS_SELECTOR, "#country").send_keys(datos.country)
    driver.find_element(By.CSS_SELECTOR, "#city").send_keys(datos.city)
    driver.find_element(By.CSS_SELECTOR, "#card").send_keys(datos.creditCard)
    driver.find_element(By.CSS_SELECTOR, "#month").send_keys(datos.month)
    driver.find_element(By.CSS_SELECTOR, "#year").send_keys(datos.year)
    driver.find_element(By.XPATH, "//button[contains(text(),'Purchase')]").click()

    # Obtener modal y validar datos
    wait = WebDriverWait(driver, 10)
    modal = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='sweet-alert  showSweetAlert visible']//p")))
    modal_text = modal.text
    fila_credit_card = modal_text.split('\n')[2]
    assert fila_credit_card == "Card Number: " + datos.creditCard



# Funcionalidades
log_in()
agregar_item(datos.Categoria.Phones)
validar_carrito()
agregar_item(datos.Categoria.Monitors)
validar_carrito()
agregar_item(datos.Categoria.Laptops)
validar_carrito()
checkout()


# Cerrar el navegador
driver.quit()
