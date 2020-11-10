import re
SIMBOLOS = "[SPRQ][0-9]*"
IMPLICACAO = "True-True"
FORMULA_TESTE = "(~Truev(False-(True-True)^False))"  # "True ^ ~False"
# resposta FORMULA_TESTE = not(True) or (not(False) or True) and False


class Arvore:
    def __init__(self, raiz):
        self.raiz = raiz


class NodoArvore:
    def __init__(self, chave):
        self.simboloProp = chave
        self.interpretacao = None
        self.esquerda = None
        self.direita = None

    def __repr__(self):
        return '%s <- %s -> %s' % (self.esquerda and self.esquerda.chave,
                                   self.chave,
                                   self.direita and self.direita.chave
                                   )

    def insere(self, noFilho):
        if noFilho.interpretacao == True:
            self.esquerda = noFilho
        elif noFilho.interpretacao == False:
            self.direita = noFilho


def calculaFormula(formula, simbolo, interpretacao):

    valor = formula.replace(simbolo, interpretacao)

    # se encontrar algum símbolo diferente de True ou False, não dá pra calcular
    if len(re.findall(SIMBOLOS, valor)) > 0:
        return None

    else:
        valor = valor.replace("v", " or ")
        valor = valor.replace("^", " and ")
        valor = valor.replace("=", " == ")

        if "-" in valor:  # só faz isso se achar implicação, senão dá erro de

            implicacao = valor.split("-")

            try:
                # se a implicação estiver entre parênteses faça:

                inicioImplicacao = implicacao[0].split("(")[-1]
                # pega o conteúdo todo antes do parênteses fechado
                fimImplicacao = implicacao[1].split(")")[0]
                print("TO AQUI", inicioImplicacao, fimImplicacao)
                valor = valor.replace(
                    inicioImplicacao+"-"+fimImplicacao, " not(" + inicioImplicacao + ") or " + fimImplicacao)
            except:
                valor = valor.replace(
                    implicacao[0]+"-"+implicacao[1], " not(" + implicacao[0] + ") or " + implicacao[1])

        if "~" in valor:
            negacao = formula.split("~")
            if negacao[1] == "(":
                fimNegacao = negacao[1].split(")")
                valor = valor.replace(
                    "~"+negacao[1], " not("+fimNegacao[0]+") ")

            else:
                if negacao[1].startswith("True"):
                    valor = valor.replace("~True", " not(True) ")
                elif negacao[1].startswith("False"):
                    valor = valor.replace("~False", " not(False) ")

    # return eval(valor)
    return formula, valor, eval(valor)


def calculaOu(formula, ladoA, ladoB):

    if ladoA == "True" or ladoB == "True":
        formula.replace(ladoA+" or "+ladoB, True)
        # return True
    else:
        formula.replace(ladoA+" or "+ladoB, False)
        # return False


def calculaNot(termo):
    if termo == "True":
        return False

    if termo == "False":
        return True


def calculaAnd(ladoA, ladoB):
    if ladoA == "False" or ladoB == "False":
        return False

    else:
        return True


if __name__ == "__main__":
    # not(True) or (not(False) or True) and False
    print(calculaFormula(FORMULA_TESTE, "P", "True"))
    print(calculaFormula(IMPLICACAO, "P", "True"))
