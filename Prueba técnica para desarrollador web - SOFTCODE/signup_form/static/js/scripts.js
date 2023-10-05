// ejecuta la funcion main despues de que cargue todo en la pagina
window.onload = () => {
    
    main();
    eliminarAlerta()
}
function eliminarAlerta(){
    // se encarga de eliminarAlerta generada desde django
    let alerta_django = document.querySelector("#alerta_django")
    if( alerta_django !== null){
        setTimeout(()=>{
            alerta_django.remove()
        },3000)
    }
}
function main(){
    // obtenemos los botones superiores ("registro", "ver todos los usuarios")
    let registro_view = document.querySelector(".signup_btn")
    let user_view = document.querySelector(".users_btn")

    // variables para no perder el html en los cambios de vista
    let form_container = document.querySelector("#form_container")
    let form_html;
    
    async function get_all_data(url){
        // args: 
        // url -> str (url a la que vamos a hacer la peticion)

        // se encarga de obtener todos los usuarios registrados
        const response = await fetch(url, {
            method:"GET"
        })
        return response
    }
    function ObtenerUsusarios(){
        // maneja la respuesta de get_all_data()
        return get_all_data("http://127.0.0.1:8000/get_all/")
        .then(response => {
            if(response.status === 200){
                return response.json()
            }
        })
        .then(data => {
            let lista_usuarios = document.createElement("div")
            lista_usuarios.classList.add("lista_cont")
            let lista = document.createElement("ul")
            lista.classList.add("lista")
            lista_usuarios.appendChild(lista)

            // Ejecuta el for solo después de que la promesa se cumpla
            for(let i = 0; i < data.length; i++){
                let dataIndex = data[i]
                let elemento = document.createElement("li")
                elemento.innerHTML = `
                <div class="card">
                    <p class="name"><span>Nombre: </span>${dataIndex.name}</p>
                    <p class="apellido"><span>Apellido: </span>${dataIndex.apellido}</p>
                    <p class="email"><span>Correo Electronico:</span> ${dataIndex.email}</p>
                    <p class="passwd"><span>Contraseña: </span>${dataIndex.password}</p>
                    <span class="actualizar"><a href="update/${dataIndex.id}"><i class='bx bxs-message-square-edit'></i></a></span>
                    <span class="eliminar"><a href="delete/${dataIndex.id}"><i class='bx bxs-trash' ></i></a></span>
                </div>
                `
                elemento.classList.add("elemento")
                lista.appendChild(elemento)
                
            }
            form_container.appendChild(lista_usuarios)
        })
    }
    registro_view.addEventListener("click", (e)=>{
        e.preventDefault()
        form_container.classList.add("form_container")
        form_container.innerHTML = form_html
    })
    user_view.addEventListener("click", (e)=>{
        e.preventDefault()
        // guardamos el contenido del body para no perderlo, para su posterior uso y limpiamos el body
        form_html = `${form_container.innerHTML}`
        form_container.innerHTML = ""
        form_container.classList.remove("form_container")

        ObtenerUsusarios()
    })
}