import git
import os
import openai
import argparse
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_git_repository():
    try:
        repo = git.Repo(os.getcwd())
        if repo.bare:
            print("No es un repositorio de Git válido.")
            return None
        return repo
    except git.exc.InvalidGitRepositoryError:
        print("No se encuentra un repositorio de Git en el directorio actual.")
        return None

def has_changes(repo):
    return bool(repo.git.diff('HEAD'))

def generate_commit_message(repo, file=None, use_ai=False):
    if file:
        file_diff = repo.git.diff('HEAD', file)
        message = f"Archivo: {file}\nCambios:\n{file_diff}\n"
    else:
        changed_files = repo.git.diff('HEAD', name_only=True).splitlines()
        if not changed_files:
            return "No hay cambios para commitear."

        message = "Detalles del commit:\n"
        for file in changed_files:
            file_diff = repo.git.diff('HEAD', file)
            message += f"\nArchivo: {file}\nCambios:\n{file_diff}\n"

    if use_ai:
        return generate_ai_description(message)

    return format_commit_message(message)

def generate_ai_description(diff_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente experto en programación. Ayuda a generar mensajes de commit siguiendo buenas prácticas. "
                        "Devuelve siempre el resultado en el siguiente formato:\n"
                        "[titulo]: <Tipo de commit como 'feat', 'fix', 'refactor', etc.>: <Título del commit>\n"
                        "[descripcion]: <Descripción detallada del commit>"
                    )
                },
                {
                    "role": "user",
                    "content": f"Analiza los siguientes cambios y genera un mensaje de commit siguiendo la plantilla proporcionada:\n{diff_text}"
                }
            ],
            max_tokens=200
        )

        ai_message = response.choices[0].message.content.strip()
        title, description = "", ""

        for line in ai_message.splitlines():
            if line.lower().startswith("[titulo]:"):
                title = line.split(":", 1)[1].strip()
            elif line.lower().startswith("[descripcion]:"):
                description = line.split(":", 1)[1].strip()

        if not title:
            title = "chore: update changes"
        if not description:
            description = "Descripción generada automáticamente no disponible."

        return f"{title}\n\n{description}"

    except Exception as e:
        print(f"Error al generar la descripción con IA: {e}")
        return "Descripción automática no disponible."

def format_commit_message(diff_text):
    if "add" in diff_text.lower():
        title = "feat: add new features"
    elif "fix" in diff_text.lower():
        title = "fix: resolve issues and bugs"
    elif "remove" in diff_text.lower():
        title = "chore: remove deprecated code"
    elif "update" in diff_text.lower() or "refactor" in diff_text.lower():
        title = "refactor: code improvements and updates"
    else:
        title = "chore: general updates"

    body = diff_text[:250].replace('\n', ' ')
    return f"{title}\n\n{body}"

def confirm_commit(commit_message):
    print("\nMensaje de commit propuesto:\n")
    print(commit_message)
    confirm = input("\n¿Deseas proceder con este commit? (s/n): ").strip().lower()
    return confirm == 's'

def commit_per_file(repo, use_ai=False):
    if not has_changes(repo):
        print("No hay cambios para commitear.")
        return

    changed_files = repo.git.diff('HEAD', name_only=True).splitlines()

    for file in changed_files:
        if not os.path.exists(file):
            print(f"Archivo {file} eliminado. Ejecutando 'git rm'.")
            try:
                repo.git.rm(file)
            except git.exc.GitCommandError as e:
                print(f"Error al eliminar {file}: {e}")
                continue
        else:
            try:
                repo.git.add(file)
            except git.exc.GitCommandError as e:
                print(f"Error al añadir {file}: {e}")
                continue

        commit_message = generate_commit_message(repo, file, use_ai)

        if confirm_commit(commit_message):
            try:
                repo.git.commit(m=commit_message)
                print(f"Commit realizado para el archivo: {file}")
            except Exception as e:
                print(f"Error al hacer el commit para {file}: {e}")
        else:
            print(f"Commit cancelado para el archivo: {file}")

def commit_all_changes(repo, use_ai=False):
    if not has_changes(repo):
        print("No hay cambios para commitear.")
        return

    try:
        repo.git.add(A=True)
        deleted_files = repo.git.diff('HEAD', name_only=True, diff_filter='D').splitlines()
        for file in deleted_files:
            print(f"Archivo {file} eliminado. Ejecutando 'git rm'.")
            repo.git.rm(file)
    except git.exc.GitCommandError as e:
        print(f"Error al preparar cambios: {e}")
        return

    commit_message = generate_commit_message(repo, use_ai=use_ai)

    if confirm_commit(commit_message):
        try:
            repo.git.commit(m=commit_message)
            print("Commit realizado con éxito para todos los cambios.")
        except Exception as e:
            print(f"Error al hacer el commit: {e}")
    else:
        print("Commit cancelado.")

def main():
    parser = argparse.ArgumentParser(description="Script para hacer commits automáticos con mensajes generados.")
    parser.add_argument(
        "--mode", choices=["per-file", "all"], default="all",
        help="Modo de commit: 'per-file' para un commit por archivo, 'all' para un solo commit con todos los cambios."
    )
    parser.add_argument(
        "--use-ai", action="store_true",
        help="Usa IA para generar descripciones detalladas de los cambios."
    )
    args = parser.parse_args()

    repo = get_git_repository()
    if not repo:
        return

    if args.mode == "per-file":
        commit_per_file(repo, use_ai=args.use_ai)
    elif args.mode == "all":
        commit_all_changes(repo, use_ai=args.use_ai)

if __name__ == "__main__":
    main()
