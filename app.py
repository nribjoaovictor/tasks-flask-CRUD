from flask import Flask, request, jsonify
from models.task import Task

# __name__ = "__main__"
app = Flask(__name__)

#rota - como vamos conseguir comunicar com o cliente - permite uma comunicação - recebe e devolve algo
#@app.route("/")
#def hello_world():
#    return "Hello, World!"

#@app.route("/about")
#def about():
#    return "Página sobre"

################################################################################################################

#CRUD - CREATE, READ, UPDATE, DELETE
#tabela: tarefa

tasks = []
task_id_control = 1
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    #request - recuperar os dados que o cliente enviou - informações
    data = request.get_json()  # Recupera os dados enviados pelo cliente em formato JSON
    new_tasks = Task(id=task_id_control,title=data['title'], description=data.get("description", ""),)
    task_id_control+=1
    tasks.append(new_tasks)
    print(tasks)
    #por padrão http, é importante retornar um formato Json e o flask tem uma biblioteca para isso, o jsonify - ajuda as APIs a controlarem
    return jsonify({
        "message": "task created successfully",
        "id": new_tasks.id,
    })


@app.route('/tasks', methods=['GET'])
def get_tasks():
    
    #1° modo para se fazer
    #task_list = []
    #for task in tasks:
    #    task_list.append(task.to_dict()) #vai retornar a task no formato que foi criado dentro do models

    #2° modo
    task_list = [task.to_dict() for task in tasks ] #criando uma nova lista com o metodo to_dict para cada task, com os elemento que ja estão dentro da lista tasks
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }
    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET']) #<int: id> - é um parâmetro que será passado na URL, e o Flask irá converter automaticamente para um inteiro - id é só um nome para identificar
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Task not found"}), 404 #404 - not found - não encontrado, é um código de status HTTP que indica que o recurso solicitado não foi encontrado no servidor.


#a função acima utiliza um parametro de rota
#parametro de rota - <int:id> - é um parâmetro que será passado na URL, e o Flask irá converter automaticamente para um inteiro
#permite que receba na rota alguma variavel do seu usuário

#os tipo de retorno podem ser: string, int, float, path, uuid(identificador único universal), path, etc
#@app.route('/user/<username>') # se quiser converter vai ser necesssario para antes, como <int:username>
#def show_user(username):
#    print(username)
#    print(type(username)) #retorna como string 
#    return f"User: {username}"


@app.route('/tasks/<int:id>', methods=['PUT']) 
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    print(task)
    if task is None:
        return jsonify({"message": "Task not found"}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)

    return jsonify({"message": "Task updated successfully"}) #como o padrão já é 200, recomenda-se não colocar o status code

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        print(t)
        if t.id == id:
            task = t
            break
    if not task :
        return jsonify({"message": "Task not found"}), 404
    tasks.remove(task)
    return jsonify({"message": "Task deleted successfully"})






#essa estrutura de chamar o programa de forma manual é importante para que o código seja executado apenas quando o arquivo for chamado diretamente, e não quando importado como um módulo.
#isso é importante para evitar que o código seja executado automaticamente quando importado, o que poderia causar comportamentos indesejados.
#apenas quando o desenvolvimento for local, o código será executado, e não quando for importado como um módulo em outro arquivo.
if __name__ == "__main__":
    app.run(debug=True) #debug habilita os logs que ajudam a identificar erros, não deve ser usado em produção
#WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead. - ao usar dessa forma.