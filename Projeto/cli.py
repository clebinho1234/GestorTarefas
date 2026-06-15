from gestor_tarefas import GestorTarefas


def menu(gestor: GestorTarefas):
    totais = gestor.contar_tarefas_por_estado()
    pendentes = gestor.contar_tarefas_por_estado("Pendente")
    concluidas = gestor.contar_tarefas_por_estado("Concluída")

    print("\nMenu de Tarefas")
    print(f"Total: {totais}")
    print(f"Pendentes: {pendentes}")
    print(f"Concluídas: {concluidas}")
    print("1 - Listar Tarefas")
    print("2 - Listar Tarefas Pendentes")
    print("3 - Listar Tarefas Concluídas")
    print("4 - Adicionar Tarefas")
    print("5 - Remover Tarefas")
    print("6 - Marcar Tarefa como concluída")
    print("7 - Editar Tarefa")
    print("0 - Sair do Programa")

def validar_titulo(tarefas):
    while True:
        titulo = input("\nDigite o novo título da tarefa: ")

        if titulo.strip() == "":
            print("Tarefa inválida, é necessário escrever algo")
        elif any(t.titulo.lower() == titulo.lower() for t in tarefas):
            print("A tarefa já existe na lista de tarefas, escreva uma nova tarefa")
        else:
            return titulo
            
def validar_prioridade():
    lista_prioridades = {
        "1": "Alta",
        "2": "Média",
        "3": "Baixa"
    }

    while True:
        prioridade_input = input("\nEscolha o número da prioridade"
                        " (1 - Alta, 2 - Média, 3 - Baixa): ")
                
        prioridade = lista_prioridades.get(prioridade_input)
                
        if prioridade:
            return prioridade
        else:
            print("Digite um valor válido")

def listar_tarefas(gestor: GestorTarefas, estado=None):
    tarefas = gestor.listar_tarefas(estado)

    if not tarefas:
        print("Não há tarefas registadas!")
        return
        
    print("\nLista de tarefas:" if not estado 
        else f"\nLista de tarefas {estado.lower()}s:")
        
    for i, tarefa in enumerate(tarefas, start=1):
        print(f"{i} - {tarefa}")

def adicionar_tarefa(gestor: GestorTarefas):
    tarefas = gestor.listar_tarefas()

    titulo = validar_titulo(tarefas)

    prioridade = validar_prioridade()

    gestor.adicionar_tarefa(titulo, prioridade)

    print("Nova tarefa adicionada!")

def remover_tarefa(gestor: GestorTarefas):
    while True:
        listar_tarefas(gestor)

        tarefas = gestor.listar_tarefas()
        
        if not tarefas:
            break

        escolha = input("\nDigite o número da tarefa a remover " \
        "ou digite 0 para regressar ao menu: ")
            
        if escolha == "0":
            break

        if escolha.isdigit():
            indice = int(escolha) - 1

            if 0 <= indice < len(tarefas):
                while True:
                    confirmacao = input("Tem certeza? (s/n)")

                    if confirmacao.lower() == "s":
                        tarefaRemovida = tarefas[indice]
                        gestor.remover_tarefa(tarefaRemovida.id)
                        print(f"Tarefa '{tarefaRemovida.titulo}' removida!")
                        break
                    elif confirmacao.lower() == "n":
                        print("Ação anulada!")
                        break
                    else:
                        print("Digite s(Sim) ou n(Nao)")
            else:
                print("Número inválido")
        else:
            print("Digite um número")

def marcar_tarefa_concluida(gestor: GestorTarefas):
    while True:
        listar_tarefas(gestor)

        tarefas = gestor.listar_tarefas()

        if not tarefas:
            break

        escolha = input("\nDigite o número da tarefa concluída " \
        "ou digite 0 para regressar ao menu: ")
            
        if escolha == "0":
            break

        if escolha.isdigit():
            indice = int(escolha) - 1

            if 0 <= indice < len(tarefas):
                if tarefas[indice].estado == "Concluída":
                    print("A tarefa já está concluída")
                else:
                    tarefa_concluida =  tarefas[indice]
                    gestor.marcar_tarefa_concluida(tarefa_concluida.id)
                    print(f"Tarefa '{tarefa_concluida.titulo}' marcada como concluída!")
            else:
                print("Número inválido")
        else:
            print("Digite um número")

def editar_tarefa(gestor: GestorTarefas):
    while True:
        listar_tarefas(gestor)

        tarefas = gestor.listar_tarefas()

        if not tarefas:
            break

        escolha = input("\nDigite o número da tarefa a editar " \
        "ou digite 0 para regressar ao menu: ")
            
        if escolha == "0":
            break

        if escolha.isdigit():
            indice = int(escolha) - 1

            if 0 <= indice < len(tarefas):
                if tarefas[indice].estado == "Concluída":
                    print("Não é possível editar uma tarefa já concluída")
                else:
                    tarefa_a_editar = tarefas[indice]

                    print("1 - Editar título")
                    print("2 - Editar prioridade")
                    escolha = input("Escolha o atributo que pretende editar: ")

                    match escolha:
                        case "1":
                            novo_titulo = validar_titulo(tarefas)
                            gestor.editar_tarefa(tarefa_a_editar.id, novo_titulo=novo_titulo)
                            print(f"Tarefa '{tarefa_a_editar.titulo}' editada para: {novo_titulo}")
                        case "2":
                            nova_prioridade = validar_prioridade()
                            gestor.editar_tarefa(tarefa_a_editar.id, nova_prioridade=nova_prioridade)
                            print(f"Prioridade da tarefa '{tarefa_a_editar.titulo}' editada para: {nova_prioridade}")
                        case _:
                            print("Número inválido")
            else:
                print("Número inválido")
        else:
            print("Digite um número")

def main():
    gestor = GestorTarefas()
    
    while True:
        menu(gestor)
        opcao = input("\nEscolha o número da opção que deseja: ")

        if opcao == "0":
            print("A fechar programa...")
            gestor.fechar_ligacao()
            break

        acoes = {
            "1": lambda g: listar_tarefas(g),
            "2": lambda g: listar_tarefas(g, "Pendente"),
            "3": lambda g: listar_tarefas(g, "Concluída"),
            "4": adicionar_tarefa,
            "5": remover_tarefa,
            "6": marcar_tarefa_concluida,
            "7": editar_tarefa
        }

        acao = acoes.get(opcao)

        if acao:
            acao(gestor)
        
            

        else:
            print(f"Valor inválido, Escolha um valor entre 0 a {len(acoes)}")

if __name__ == "__main__":
    main()