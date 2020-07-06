from django.test import TestCase

from clientes.models import Cliente, Marca, Contacto


class ClienteTest(TestCase):

    def crear_cliente(self, razon_social="Caño oxígeno"):
        return Cliente.objects.create(razon_social=razon_social)

    def test_cliente_creacion(self):
        c = self.crear_cliente()
        self.assertTrue(isinstance(c, Cliente))
        self.assertEqual(c.__str__(), c.razon_social)


class MarcaTest(TestCase):

    def crear_marca(self):
        cliente = Cliente.objects.create(razon_social="ñá prueba")
        return Marca.objects.create(cliente=cliente, nombre='Año de pruebá')

    def test_creacion_marca(self):
        m = self.crear_marca()
        self.assertTrue(isinstance(m, Marca))
        self.assertEqual(m.__str__(), m.nombre)


class ContactoTest(TestCase):

    def crear_contacto(self):
        cliente = Cliente.objects.create(razon_social="ñá prueba")
        return Contacto.objects.create(cliente=cliente, nombre='Contacto pruebá año')

    def test_creacion_marca(self):
        c = self.crear_contacto()
        self.assertTrue(isinstance(c, Contacto))
        self.assertEqual(c.__str__(), c.nombre)
