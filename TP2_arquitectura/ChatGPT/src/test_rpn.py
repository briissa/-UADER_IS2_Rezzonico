import unittest
import math
from rpn import RPNCalculator, RPNError

class TestRPNCalculator(unittest.TestCase):
    
    def setUp(self):
        """Crear una nueva calculadora antes de cada test"""
        self.calc = RPNCalculator()
    
    # ========== TESTS DE OPERACIONES BÁSICAS ==========
    
    def test_suma(self):
        resultado = self.calc.ejecutar("3 4 +")
        self.assertEqual(resultado, 7.0)
    
    def test_resta(self):
        resultado = self.calc.ejecutar("10 3 -")
        self.assertEqual(resultado, 7.0)
    
    def test_multiplicacion(self):
        resultado = self.calc.ejecutar("5 6 *")
        self.assertEqual(resultado, 30.0)
    
    def test_division(self):
        resultado = self.calc.ejecutar("15 3 /")
        self.assertEqual(resultado, 5.0)
    
    def test_expresion_compuesta(self):
        resultado = self.calc.ejecutar("5 1 2 + 4 * + 3 -")
        self.assertEqual(resultado, 14.0)
    
    def test_expresion_compuesta2(self):
        resultado = self.calc.ejecutar("2 3 4 * +")
        self.assertEqual(resultado, 14.0)
    
    # ========== TESTS DE NUMEROS ENTEROS Y REALES ==========
    
    def test_numero_entero(self):
        resultado = self.calc.ejecutar("42")
        self.assertEqual(resultado, 42.0)
    
    def test_numero_real(self):
        resultado = self.calc.ejecutar("3.1416")
        self.assertEqual(resultado, 3.1416)
    
    def test_numero_negativo(self):
        resultado = self.calc.ejecutar("-5 3 +")
        self.assertEqual(resultado, -2.0)
    
    # ========== TESTS DE ERRORES ==========
    
    def test_error_token_invalido(self):
        with self.assertRaises(RPNError) as context:
            self.calc.ejecutar("3 4 $")
        self.assertIn("Token inválido", str(context.exception))
    
    def test_error_pila_insuficiente(self):
        with self.assertRaises(RPNError) as context:
            self.calc.ejecutar("3 +")
        self.assertIn("Pila insuficiente", str(context.exception))
    
    def test_error_division_cero(self):
        with self.assertRaises(RPNError) as context:
            self.calc.ejecutar("3 0 /")
        self.assertIn("División por cero", str(context.exception))
    
    def test_error_pila_final_multiple(self):
        with self.assertRaises(RPNError) as context:
            self.calc.ejecutar("3 4 5 +")
        self.assertIn("debe quedar con 1 elemento", str(context.exception))
    
    # ========== TESTS DE COMANDOS DE PILA ==========
    
    def test_dup(self):
        resultado = self.calc.ejecutar("5 dup *")
        self.assertEqual(resultado, 25.0)
    
    def test_swap(self):
        resultado = self.calc.ejecutar("3 4 swap -")
        self.assertEqual(resultado, 1.0)  # 4 - 3 = 1
    
    def test_drop(self):
        resultado = self.calc.ejecutar("5 10 drop")
        self.assertEqual(resultado, 5.0)
    
    def test_clear(self):
        resultado = self.calc.ejecutar("1 2 3 clear 5")
        self.assertEqual(resultado, 5.0)
    
    # ========== TESTS DE CONSTANTES ==========
    
    def test_constante_pi(self):
        resultado = self.calc.ejecutar("pi")
        self.assertEqual(resultado, math.pi)
    
    def test_constante_e(self):
        resultado = self.calc.ejecutar("e")
        self.assertEqual(resultado, math.e)
    
    def test_constante_phi(self):
        resultado = self.calc.ejecutar("phi")
        phi_esperado = (1 + math.sqrt(5)) / 2
        self.assertEqual(resultado, phi_esperado)
    
    # ========== TESTS DE FUNCIONES MATEMATICAS ==========
    
    def test_sqrt(self):
        resultado = self.calc.ejecutar("16 sqrt")
        self.assertEqual(resultado, 4.0)
    
    def test_log(self):
        resultado = self.calc.ejecutar("100 log")
        self.assertEqual(resultado, 2.0)
    
    def test_ln(self):
        resultado = self.calc.ejecutar("2.718281828459045 ln")
        self.assertAlmostEqual(resultado, 1.0, places=5)
    
    def test_exp(self):
        resultado = self.calc.ejecutar("1 e^x")
        self.assertAlmostEqual(resultado, math.e, places=5)
    
    def test_potencia_yx(self):
        resultado = self.calc.ejecutar("2 3 y^x")
        self.assertEqual(resultado, 8.0)
    
    def test_inverso(self):
        resultado = self.calc.ejecutar("4 1/x")
        self.assertEqual(resultado, 0.25)
    
    def test_chs(self):
        resultado = self.calc.ejecutar("10 CHS")
        self.assertEqual(resultado, -10.0)
    
    # ========== TESTS DE TRIGONOMETRIA (GRADOS) ==========
    
    def test_sin(self):
        resultado = self.calc.ejecutar("90 sin")
        self.assertEqual(resultado, 1.0)
    
    def test_cos(self):
        resultado = self.calc.ejecutar("0 cos")
        self.assertEqual(resultado, 1.0)
    
    def test_tg(self):
        resultado = self.calc.ejecutar("45 tg")
        self.assertAlmostEqual(resultado, 1.0, places=5)
    
    def test_asin(self):
        resultado = self.calc.ejecutar("1 asin")
        self.assertEqual(resultado, 90.0)
    
    def test_acos(self):
        resultado = self.calc.ejecutar("0 acos")
        self.assertEqual(resultado, 90.0)
    
    def test_atg(self):
        resultado = self.calc.ejecutar("1 atg")
        self.assertEqual(resultado, 45.0)
    
    # ========== TESTS DE MEMORIAS ==========
    
    def test_sto_rcl(self):
        resultado = self.calc.ejecutar("42 STO 05 RCL 05")
        self.assertEqual(resultado, 42.0)
    
    def test_multiples_memorias(self):
    # Cada ejecutar() debe dejar exactamente 1 elemento
        self.calc.ejecutar("10 STO 00 10")  # Deja 10 en la pila
        self.calc.ejecutar("20 STO 01 20")  # Deja 20 en la pila
        resultado = self.calc.ejecutar("RCL 00 RCL 01 +")
        self.assertEqual(resultado, 30.0)
    
    def test_memoria_09(self):
        resultado = self.calc.ejecutar("99 STO 09 RCL 09")
        self.assertEqual(resultado, 99.0)
    
    # ========== TESTS DE OPERACIONES ENCADENADAS ==========
    
    def test_operaciones_multiples(self):
        resultado = self.calc.ejecutar("2 3 + 4 * 5 /")
        self.assertEqual(resultado, 4.0)
    
    def test_combinacion_funciones(self):
        resultado = self.calc.ejecutar("4 sqrt 3 +")
        self.assertEqual(resultado, 5.0)

if __name__ == "__main__":
    unittest.main()