from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
action_chains = ActionChains(driver=driver)

driver.get("https://serviciosturisticos.mendoza.gov.ar/sistema/agente/")

wait = WebDriverWait(driver, 5)

usuario = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "input[type='text']")))
usuario.click()
usuario.send_keys("mguerra")
password = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "input[placeholder='Contraseña']")))
password.click()
password.send_keys("mguerra123")

submit = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "button[type='submit']"))).click()

vademecum = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "a[id='vadem']"))).click()

# ENTRA A ALOJAMIENTOS
alojamientos_tab = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "tr[id='rubros_datagrid-row-r2-2-1']"))).click()

# ENTRA A AGENCIAS
""" alojamientos_tab = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "tr[id='rubros_datagrid-row-r2-2-0']"))).click() """

paginas = 58  # 24 en agencias
index = 0
alojamientos_vademecum = []

agencias_vademecum = []

try:
    while index < paginas:

        alojamientos = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table[contains(@class, 'datagrid-btable')][.//tr[contains(@id, 'registros_datagrid-row')]]//tr[not(@style='background-color:#C285C2;color:#fff;')]")))

        # agencias = wait.until(EC.presence_of_all_elements_located(
        #    (By.XPATH, "//table[contains(@class, 'datagrid-btable')][.//tr[contains(@id, 'registros_datagrid-row')]]//tr[not(@style='background-color:#C285C2;color:#fff;')]")))

        for a in alojamientos:

            try:

                action_chains.double_click(a).perform()
                time.sleep(2)
                id = wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                    "//input[@class='textbox-value' and @name='legajo' and @type='hidden']")
                )).get_attribute("value")
                print(f"ID: {id}")

                nombre = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@class='textbox-value' and @name='nombre' and @type='hidden']"))).get_attribute("value")
                print(f"Nombre: {nombre}")

                habitaciones = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@class='textbox-value' and @name='cantidad_habit' and @type='hidden']"))).get_attribute("value")
                print(f"Habitaciones: {habitaciones}")

                parcelas = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@class='textbox-value' and @name='cantidad_parcelas' and @type='hidden']"))).get_attribute("value")
                print(f"Parcelas: {parcelas}")

                plazas = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@class='textbox-value' and @name='cantidad_plazas' and @type='hidden']"))).get_attribute("value")
                print(f"Plazas: {plazas}")

                cabañas = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@class='textbox-value' and @name='cantidad_cabanias' and @type='hidden']"))).get_attribute("value")
                print(f"Cabañas: {cabañas}")

                fecha_inscripcion = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@class='textbox-value' and @name='fecha_inscripcion' and @type='hidden']"))).get_attribute("value")
                print(f"Fecha de inscripción: {fecha_inscripcion}")

                departamento = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@class='textbox-value' and @name='depto' and @type='hidden']"))).get_attribute("value")
                print(f"Departamento: {departamento}")

                clasificacion = wait.until(EC.presence_of_element_located(
                    # name='clase' en alojamientos
                    (By.XPATH, "//input[@class='textbox-value' and @name='clase' and @type='hidden']"))).get_attribute("value")
                print(f"Clasificación: {clasificacion}")

                localidad = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@class='textbox-value' and @name='localidad' and @type='hidden']"))).get_attribute("value")
                print(f"Localidad: {localidad}")

                """ tipo = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[7]/div[2]/form/table[2]/tbody/tr[6]/td[1]/span[1]/input"))).get_attribute("value") """
                alojamientos_vademecum.append(
                    [id, nombre, habitaciones, parcelas, plazas, cabañas, fecha_inscripcion, departamento, clasificacion, localidad])
                
            except Exception as e:
                print(f"Error al obtener el alojamiento: {e}")
                continue

            cerrar = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[7]/div[1]/div[2]/a"))).click()

        index = index + 1
        paginado = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "span[class='l-btn-icon pagination-next']"))).click()
        time.sleep(1)
except:
    pass

driver.quit()

# Guardar los datos en un archivo CSV con pandas
columnas = ["ID", "Nombre", "Habitaciones", "Parcelas", "Plazas", "Cabañas",
            "Fecha Inscripción", "Departamento", "Clasificación", "Localidad"]
df = pd.DataFrame(alojamientos_vademecum, columns=columnas)
df.to_csv("alojamientos.csv", index=False, encoding="utf-8", mode="a")
print("Datos guardados en 'alojamientos.csv'")
