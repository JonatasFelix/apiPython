async function carregarClientes() {
const response = await axios.get("http://127.0.0.1:8000/clientes")
const clientes = response.data
const listaClientes = document.getElementById("lista_clientes")
clientes.forEach(cliente => {
    const item = document.createElement('li')
    item.innerText = `ID: ${cliente.id} - Nome: ${cliente.nome} ${cliente.sobrenome}`
    listaClientes.appendChild(item)
});

}

function maniForm() {
    const formCadastro = document.getElementById('formulario')
    const inputNome = document.getElementById('nome')
    const inputSobrnome = document.getElementById('sobrenome')
    const inputEmail = document.getElementById('email')
    const inputFone = document.getElementById('fone')
    const inputEstado = document.getElementById('estado')
    const inputCidade = document.getElementById('cidade')
    formCadastro.onsubmit = async (event) => {
        event.preventDefault()
        const nomeCliente = inputNome.value
        const sobrenomeCliente = inputSobrnome.value
        const emailCliente = inputEmail.value
        const foneCliente = inputFone.value
        const estadoCliente = inputEstado.value
        const cidadeCliente = inputCidade.value
        await axios.post('http://127.0.0.1:8000/cadastrar/', {
            nome: nomeCliente,
            sobrenome: sobrenomeCliente,
            email: emailCliente,
            fone: foneCliente,
            estado: estadoCliente,
            cidade: cidadeCliente,
        })

        alert('Cliente cadastrado com sucesso!')

    }
}



async function deleteDataById() {
    const formDelet = document.getElementById('formulario_delete')
    const id = document.getElementById("deleteid").value;
    const idString = id.toString();
    formDelet.onsubmit = async (event) => {
        event.preventDefault()
        try {
        const res = await axios.delete(`http://127.0.0.1:8000/clientes/${idString}`);
        alert('APAGADO COM SUCESSO')
        } catch (err) {
            console.log(id)
            alert('error')

        }
    };
  }


  async function consultarDataById() {
    const formCons = document.getElementById('formulario_consultar')
    const result = document.getElementById('result_id')
    const id = document.getElementById("consultarid").value;
    const idString = id.toString();
    formCons.onsubmit = async (event) => {
        event.preventDefault()
        try {
        const res = await axios.get(`http://127.0.0.1:8000/clientes/${idString}`);
        const cliente = res.data
        const item = document.createElement('li')
        item.innerText = `ID: ${cliente.id} - Nome: ${cliente.nome} ${cliente.sobrenome}`
        result.appendChild(item)
        } catch (err) {
            console.log(id)
            alert('ID não localizado!')
        }
    };
  }




function app() {
    console.log("API INICIADA COM SUCESSO!")
    carregarClientes()
    maniForm()
}

app()