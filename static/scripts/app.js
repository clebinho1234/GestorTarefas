let editId = null;

        async function listar() {
            const response = await fetch("/tarefas");
            const tarefas = await response.json();

            const tabela = document.getElementById("tabela");
            tabela.innerHTML = "";

            tarefas.forEach(t => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${t.id}</td>
                    <td>${t.titulo}</td>
                    <td>${t.prioridade}</td>
                    <td>${t.data_criacao}</td>
                    <td>${t.estado}</td>
                    <td>
                        <button class="btn-edit" onclick="abrirModal(${t.id}, '${t.titulo}', '${t.prioridade}')">Editar</button>
                        <button class="btn-delete" onclick="apagar(${t.id})">Apagar</button>
                        <button class="btn-concluir" onclick="concluir(${t.id})">Concluir</button>
                    </td>
                `;
                tabela.appendChild(tr);
            });
        }

        async function adicionar() {
            const titulo = document.getElementById("titulo").value;
            const prioridade = document.getElementById("prioridade").value;

            await fetch("/tarefas", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ titulo, prioridade })
            });

            listar();
        }

        async function apagar(id) {
            await fetch(`/tarefas/${id}`, {
                method: "DELETE"
            });

            listar();
        }

        async function concluir(id) {
            await fetch(`/tarefas/${id}`, {
                method: "PUT"
            });

            listar();
        }

        function abrirModal(id, titulo, prioridade) {
            editId = id;

            document.getElementById("modal-titulo").value = titulo;
            document.getElementById("modal-prioridade").value = prioridade;

            document.getElementById("modal").style.display = "block";
        }

        async function guardarEdicao() {
            if (!editId) return;

            const titulo = document.getElementById("modal-titulo").value;
            const prioridade = document.getElementById("modal-prioridade").value;

            await fetch(`/tarefas/${editId}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({titulo, prioridade})
            });

            fecharModal();
            listar();
        }

        function fecharModal() {
            document.getElementById("modal").style.display = "none";
            editId = null;
        }

        listar();