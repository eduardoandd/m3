# main
from interface import MenuPrincipal

if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()


'''
MELHORIAS A FAZER:

- Quero que seja possível digitar o nome de ambos os campos, 
pra fazer a procura, e caso não exista, ao tentar cadastrar, 
deve retornar uma mensagem com algo do tipo "Cliente não encontrado. 
Necessário realizar o cadastro do mesmo ou apenas revise se o nome está correto" 
e o mesmo quero para o campo veículo.

- Arrumar a questão das datas na entidade Locações, pois estão ficando como "None"

- Colocar imagens e ícones

'''