# Estrutura de dados para armazenar os alunos
alunos = []

# Contador de matrículas por curso
contador_matriculas = {}


def gerar_matricula(curso):
    
     # Gera uma matrícula automática baseada no curso.
    
    curso = curso.upper()
    
    if curso not in contador_matriculas:
        contador_matriculas[curso] = 1
    else:
        contador_matriculas[curso] += 1
    
    return f"{curso}{contador_matriculas[curso]}"


def criar_aluno():
    
     # Cadastra um novo aluno no sistema.
    
    print("\n=== CADASTRAR NOVO ALUNO ===")
    
    nome = input("Nome do aluno: ").strip()
    if not nome:
        print("❌ Nome não pode estar vazio!")
        return
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Email não pode estar vazio!")
        return
    
    print("\nCursos disponíveis: GES, GEC, GET, GEP, etc.")
    curso = input("Curso (sigla): ").strip().upper()
    if not curso:
        print("❌ Curso não pode estar vazio!")
        return
    
    # Gerar a matrícula 
    matricula = gerar_matricula(curso)
    
   
    aluno = {
        'nome': nome,
        'email': email,
        'curso': curso,
        'matricula': matricula
    }
    
    alunos.append(aluno)
    print(f"\n✅ Aluno cadastrado com sucesso!")
    print(f"   Matrícula gerada: {matricula}")


def listar_alunos():
    """
    Lista todos os alunos cadastrados.
    """
    print("\n=== LISTA DE ALUNOS ===")
    
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    
    print(f"\nTotal de alunos: {len(alunos)}\n")
    print("-" * 80)
    print(f"{'Matrícula':<12} {'Nome':<25} {'Email':<30} {'Curso':<8}")
    print("-" * 80)
    
    for aluno in alunos:
        print(f"{aluno['matricula']:<12} {aluno['nome']:<25} {aluno['email']:<30} {aluno['curso']:<8}")
    
    print("-" * 80)


def buscar_aluno_por_matricula(matricula):
   
    for aluno in alunos:
        if aluno['matricula'] == matricula.upper():
            return aluno
    return None


def atualizar_aluno():
   
    print("\n=== ATUALIZAR ALUNO ===")
    
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    
    matricula = input("Digite a matrícula do aluno: ").strip().upper()
    aluno = buscar_aluno_por_matricula(matricula)
    
    if not aluno:
        print(f"❌ Aluno com matrícula {matricula} não encontrado!")
        return
    
    print(f"\nAluno encontrado:")
    print(f"  Nome: {aluno['nome']}")
    print(f"  Email: {aluno['email']}")
    print(f"  Curso: {aluno['curso']}")
    print(f"  Matrícula: {aluno['matricula']}")
    
    print("\n--- Digite os novos dados  ---")
    
    novo_nome = input(f"Novo nome [{aluno['nome']}]: ").strip()
    if novo_nome:
        aluno['nome'] = novo_nome
    
    novo_email = input(f"Novo email [{aluno['email']}]: ").strip()
    if novo_email:
        aluno['email'] = novo_email
    
    novo_curso = input(f"Novo curso [{aluno['curso']}]: ").strip().upper()
    if novo_curso:
       
        if novo_curso != aluno['curso']:
            aluno['curso'] = novo_curso
            nova_matricula = gerar_matricula(novo_curso)
            print(f"⚠️  Curso alterado. Nova matrícula gerada: {nova_matricula}")
            aluno['matricula'] = nova_matricula
    
    print("\n✅ Aluno atualizado com sucesso!")


def deletar_aluno():
   
    print("\n=== DELETAR ALUNO ===")
    
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    
    matricula = input("Digite a matrícula do aluno: ").strip().upper()
    aluno = buscar_aluno_por_matricula(matricula)
    
    if not aluno:
        print(f"❌ Aluno com matrícula {matricula} não encontrado!")
        return
    
    print(f"\nAluno encontrado:")
    print(f"  Nome: {aluno['nome']}")
    print(f"  Email: {aluno['email']}")
    print(f"  Curso: {aluno['curso']}")
    print(f"  Matrícula: {aluno['matricula']}")
    
    confirmacao = input("\n⚠️  Tem certeza que deseja deletar este aluno? (s/n): ").strip().lower()
    
    if confirmacao == 's':
        alunos.remove(aluno)
        print("\n✅ Aluno deletado com sucesso!")
    else:
        print("\n❌ Operação cancelada.")


def exibir_menu():
    
    print("\n" + "=" * 50)
    print("  SISTEMA DE GERENCIAMENTO DE ALUNOS")
    print("=" * 50)
    print("1. Cadastrar novo aluno")
    print("2. Listar todos os alunos")
    print("3. Atualizar aluno")
    print("4. Deletar aluno")
    print("5. Sair")
    print("=" * 50)


def main():
    
    print("\n🎓 Bem-vindo ao Sistema de Gerenciamento de Alunos!")
    
    while True:
        exibir_menu()
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            criar_aluno()
        elif opcao == '2':
            listar_alunos()
        elif opcao == '3':
            atualizar_aluno()
        elif opcao == '4':
            deletar_aluno()
        elif opcao == '5':
            print("\n👋 Encerrando o sistema. Até logo!")
            break
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção entre 1 e 5.")
        
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
