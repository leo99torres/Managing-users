// Função para buscar e exibir todos os usuários da API
function carregarUsuarios() {
  const tabela = document.querySelector("#tabelaUsuarios tbody"); // Seleciona o corpo da tabela
  if (!tabela) return; // Se a tabela não existir, sai da função

  tabela.innerHTML = ""; // Limpa o conteúdo da tabela antes de preencher

 //fetch é uma função do JavaScript que faz requisições HTTP para servidores.

  // Faz uma requisição GET para buscar os usuários
  fetch("http://localhost:8000/users")
    .then(res => res.json()) // Converte a resposta para JSON
    .then(usuarios => {
      usuarios.forEach(usuario => {
        // Cria uma nova linha na tabela
        const linha = document.createElement("tr");
        linha.innerHTML = `
          <td class="text-center border-b border-gray-700">${usuario.name}</td>
          <td class="text-center border-b border-gray-700">${usuario.email}</td>
          <td class="text-center border-b border-gray-700">${usuario.phone}</td>
          <td class="text-center border-b border-gray-700">${usuario.role ?? ""}</td>
        `;
        tabela.appendChild(linha); // Adiciona a linha à tabela
      });
    })
    .catch(err => {
      console.error("Erro ao carregar usuários:", err); // Se der erro, exibe no console
    });
}

// Função para cadastrar um novo usuário
function cadastrarUsuario(event) {
  event.preventDefault(); // Evita o recarregamento da página

  // Monta o objeto com os dados do novo usuário escrito na tela
  const novoUsuario = {
    name: document.getElementById("nome").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("telefone").value.replace(/\D/g, ""), // Remove qualquer caractere que não seja número
    role: document.getElementById("role").value || null
  };

  // Envia a requisição POST para cadastrar o usuário
  fetch("http://localhost:8000/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(novoUsuario)
  }) //Isso envia os dados do novo usuário para o backend.
    .then(response => {
      if (!response.ok) {
        // Se o backend retornar erro, extrai a mensagem do erro e lança
        return response.json().then(data => {
          const msg = Array.isArray(data.detail)
            ? data.detail.map(e => e.msg.replace(/^Value error,\s*/, '')).join("; ")
            : typeof data.detail === 'string'
              ? data.detail
              : "Erro inesperado.";
          throw new Error(msg);
        });
      }
      return response.json(); // Se estiver tudo certo, segue o fluxo
    })
    .then(data => {
      // Exibe mensagem de sucesso, reseta o formulário e atualiza a tabela
      mostrarMensagem("mensagemCadastro", "Usuário cadastrado com sucesso!", "green");
      document.getElementById("formCadastro").reset();
      carregarUsuarios();
    })
    .catch(err => {
      // Mostra mensagem de erro se algo falhar
      mostrarMensagem("mensagemCadastro", `Erro: ${err.message}`, "red");
    });
}

// Função para atualizar os dados de um usuário
function atualizarUsuario(event) {
  event.preventDefault(); // Impede o reload da página

  const email = document.getElementById("edit_email").value; // Pega o email da tela como identificador unico

  
  const dadosAtualizados = {};//objeto vazio

  // Prepara os dados a serem atualizados
  const nome = document.getElementById("edit_nome").value;
  const telefone = document.getElementById("edit_telefone").value.replace(/\D/g, "");
  const role = document.getElementById("edit_role").value;

  if (nome) dadosAtualizados.name = nome;
  if (telefone) dadosAtualizados.phone = telefone;
  if (role) dadosAtualizados.role = role;

  // Se nenhum campo foi preenchido, alerta o usuário
  if (Object.keys(dadosAtualizados).length === 0) {
    alert("Preencha ao menos um campo para atualizar.");
    return;
  }

  // Envia requisição PUT para atualizar o usuário
  fetch(`http://localhost:8000/users/by-email/${encodeURIComponent(email)}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(dadosAtualizados)
  })
    .then(response => {
      if (!response.ok) {
        // Trata erro da resposta
        return response.json().then(data => {
          const msg = Array.isArray(data.detail)
            ? data.detail.map(e => e.msg).join("; ")
            : typeof data.detail === 'string'
              ? data.detail
              : "Erro inesperado.";
          throw new Error(msg);
        });
      }

      // Exibe sucesso, reseta formulário e recarrega a tabela
      mostrarMensagem("mensagemEdicao", "Usuário atualizado com sucesso!", "green");
      document.getElementById("formEdicao").reset();
      carregarUsuarios();
    })
    .catch(err => {
      mostrarMensagem("mensagemEdicao", `Erro: ${err.message}`, "red");
    });
}

// Função para deletar um usuário pelo email
function deletarUsuario(event) {
  event.preventDefault();

  const email = document.getElementById("delete_email").value;

  // Requisição DELETE com base no e-mail
  fetch(`http://localhost:8000/users/by-email/${encodeURIComponent(email)}`, {
    method: "DELETE"
  })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          const msg = Array.isArray(data.detail)
            ? data.detail.map(e => e.msg).join("; ")
            : typeof data.detail === 'string'
              ? data.detail
              : "Erro inesperado.";
          throw new Error(msg);
        });
      }

      // Exibe sucesso e atualiza tabela
      mostrarMensagem("mensagemDelete", "Usuário excluído com sucesso!", "green");
      document.getElementById("formDelete").reset();
      carregarUsuarios();
    })
    .catch(err => {
      mostrarMensagem("mensagemDelete", `Erro: ${err.message}`, "red");
    });
}

// Função utilitária para exibir mensagens com animação
function mostrarMensagem(id, texto, cor) {
  const msg = document.getElementById(id);
  msg.innerText = texto;
  msg.style.color = cor;
  msg.classList.remove("hidden");
  msg.classList.add("opacity-100", "transition-opacity", "duration-500");

  // Some a mensagem após 3 segundos
  setTimeout(() => {
    msg.classList.remove("opacity-100");
    msg.classList.add("opacity-0");

    setTimeout(() => {
      msg.innerText = "";
      msg.classList.remove("opacity-0", "transition-opacity", "duration-500");
    }, 500);
  }, 3000);
}
