import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


#Clase de seccion para agregar direccion desde y hasta
class UrbanRoutesPage:
    #Indicar Marcadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    #Generar constructor
    def __init__(self, driver):
        self.driver = driver

    #Generar Accion
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def click_final(self):
        self.driver.find_element(*self.start_button).clik()

    #Accion en un paso
    def send_adres(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)


#Definir clase para seccion de inicio de viaje
class StartTrip:
    #Marcador de boton solicitar un taxi
    start_button = (By.XPATH, ".//div[@class='results-text']/button[@class='button round']")

    def __init__(self, driver):
        self.driver = driver

    def start_trip(self):
        self.driver.find_element(*self.start_button).click()


#Definir  una clase para la seleccion de tipo de viaje y seleccion de telefono
class TravelMode:
    #Selector de modo de viaje comfort
    comfort_button = (By.XPATH, ".//img[@src='/static/media/kids.075fd8d4.svg']")
    #Selector para ingresar un numero telefonico
    add_phone_button = (By.CLASS_NAME, "np-button")

    def __init__(self, driver):
        self.driver = driver

    def clic_on_comfort_button(self):
        self.driver.find_element(*self.comfort_button).click()

    def click_in_new_phone(self):
        self.driver.find_element(*self.add_phone_button).click()

    def comford_and_number(self):
        self.clic_on_comfort_button()
        self.click_in_new_phone()


#Definir una clase para agregar numero telefónico
class NewPhonRegister:
    space_new_number = (By.ID, "phone")
    next_button = (By.CLASS_NAME, "buttons")

    def __init__(self, driver):
        self.driver = driver

    def whrite_new_phone(self, phone):
        self.driver.find_element(*self.space_new_number).send_keys(phone)

    def click_in_next(self):
        self.driver.find_element(*self.next_button).click()

    def add_new_phone(self, phone):
        self.whrite_new_phone(phone)
        self.click_in_next()


#Correr codigo para obtener codigo de verificación


#Confirmacion por de numero telefónico:
class ConfirmCode:
    code_confirmation = (By.ID, "code")
    confirmation = (By.CSS_SELECTOR, ".//button[text()='Confirm']")

    def __init__(self, driver):
        self.driver = driver

    def validation_code(self, code):
        self.driver.find_element(*self.code_confirmation).send_keys(code)

    def clic_in_confirm(self):
        self.driver.find_element(*self.confirmation).click()

    def final_confirmation(self, code):
        self.validation_code(code)
        self.clic_in_confirm()


#Agregar numero de tarjeta:
class AddCredithCard:
    Card_Number = (By.ID, "number")
    cvv = (By.ID, "code")
    add_button = (By.XPATH, ".//div[@class='pp-buttons'/button[@type='submit']")

    def __init__(self, driver):
        self.driver = driver

    def wrhite_number_card(self, number):
        self.driver.find_element(*self.Card_Number).send_keys(number)

    def click_in_cvv(self):
        self.driver.find_element(*self.cvv).click()

    def whrite_card_cvv(self, cvv):
        self.driver.find_element(*cvv).send_keys(cvv)

    def finaly_card(self):
        self.driver.find_element(*self.add_button).clock()

    def send_card_information(self, number, cvv):
        self.wrhite_number_card(number)
        self.click_in_cvv()
        self.whrite_card_cvv(cvv)
        self.finaly_card()


#Crear una clase para mandar un mensaje
class SendMessage:
    message = (By.ID, "comment")
    blanket_and_scarver_button = (By.CLASS_NAME, "slider round")
    icecream_button = (By.CSS_SELECTOR, "counter-plus")
    start_new_travel = (By.CLASS_NAME, "smart-button-secondary")

    def __init__(self, driver):
        self.driver = driver

    def send_a_message(self, message):
        self.driver.find_element(*self.message).send_keys(message)

    def ask_blanket(self):
        self.driver.find_element(*self.blanket_and_scarver_button).click()

    def ask_icecream_1(self):
        self.driver.find_element(*self.icecream_button).click()

    def ask_icecream_2(self):
        self.driver.find_element(*self.icecream_button).click()

    def start_new_trave(self):
        self.driver.find_element(*self.start_new_travel).click()

    def final_step(self, message):
        self.send_a_message(message)
        self.ask_blanket()
        self.ask_icecream_1()
        self.ask_icecream_2()
        self.start_new_trave()


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)

        #Crear una clase de objeto para colocar datos desde y hasta
        data_travel = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, "from")))
        traver_from = data.address_from
        travel_to = data.address_to
        data_travel.send_adres(traver_from, travel_to)
        # Clic para solicitar viaje
        WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, ".//div[@class='results-text']/button[@class='button round']")))
        ask_taxy = StartTrip(self.driver)
        ask_taxy.start_trip()
        #registrar modalidad de viaje e iniciar a cargar telefono nuevo
        WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable((By.XPATH, ".//img[@src='/static/media/kids.075fd8d4.svg']")))
        options_travel = TravelMode(self.driver)
        options_travel.comford_and_number()
        #registrar telefono nuevo
        WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable((By.ID, "phone")))
        registration_phone = NewPhonRegister(self.driver)
        data_phone = data.phone_number
        registration_phone.add_new_phone(data_phone)
        WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable((By.XPATH, ".//button[text()='Confirm']")))

        #Confirmar codigo de verificación
        def get_code(self):
            get_phone_code = retrieve_phone_code(self)
            return self.driver.find_element(By.ID, "code").send_keys(get_phone_code)
        self.driver.find_element(By.XPATH, ".//button[text()='Confirm']").click()
        WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable(By.CLASS_NAME, "pp-button filled"))
        self.driver.find_element(By.CLASS_NAME, "pp-button filled").click()

        data_credit_card = AddCredithCard(self.driver)
        number_card = data.card_number
        number_cvv = data.card_code
        data_credit_card.send_card_information(number_card, number_cvv)

        # Realizar comentarios finales del pedido
        WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable((By.ID, "comment")))
        send_final = SendMessage
        message = data.message_for_driver
        send_final.final_step(self, message)
