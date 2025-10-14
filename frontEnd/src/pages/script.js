export const API_BASE_URL = "http://127.0.0.1:8000";

// ---------- utilitários ----------
function authHeader() {
    const token = localStorage.getItem("access_token");
    return token ? { "Authorization": "Bearer " + token } : {};
}

async function request(url, options = {}) {
    const headers = Object.assign(
        { "Content-Type": "application/json" },
        options.headers || {},
        authHeader()
    );
    const res = await fetch(API_BASE_URL + url, { ...options, headers });
    if (res.status === 204) return null;
    const data = await res.json().catch(() => null);
    if (!res.ok) {
        const err = data?.detail || data?.mensagem || data || res.statusText;
        throw new Error(err);
    }
    return data;
}

// ---------- Login / Register (index.html) ----------
if (document.getElementById("form-login")) {
    const formLogin = document.getElementById("form-login");
    const formRegister = document.getElementById("form-register");
    const btnShowLogin = document.getElementById("btn-show-login");
    const btnShowRegister = document.getElementById("btn-show-register");
    const authMessage = document.getElementById("auth-message");

    btnShowLogin.onclick = () => {
        btnShowLogin.classList.add("active");
        btnShowRegister.classList.remove("active");
        formLogin.classList.remove("hidden");
        formRegister.classList.add("hidden");
    };
    btnShowRegister.onclick = () => {
        btnShowRegister.classList.add("active");
        btnShowLogin.classList.remove("active");
        formRegister.classList.remove("hidden");
        formLogin.classList.add("hidden");
    };

    formLogin.addEventListener("submit", async (e) => {
        e.preventDefault();
        authMessage.textContent = "";
        try {
            const email = document.getElementById("login-email").value.trim();
            const password = document.getElementById("login-password").value;
            const data = await request("/auth/login", {
                method: "POST",
                body: JSON.stringify({ email, password }),
            });
            // salva token
            localStorage.setItem("access_token", data.access_token);
            window.location.href = "dashboard.html";
        } catch (err) {
            authMessage.textContent = err.message;
        }
    });

    formRegister.addEventListener("submit", async (e) => {
        e.preventDefault();
        authMessage.textContent = "";
        try {
            const name = document.getElementById("register-name").value.trim();
            const email = document.getElementById("register-email").value.trim();
            const password = document.getElementById("register-password").value;
            const admin = document.getElementById("register-admin").checked; // ✅ novo campo

            const data = await request("/auth/register", {
                method: "POST",
                body: JSON.stringify({ name, email, password, admin }), // ✅ envia o campo admin
            });

            authMessage.style.color = "var(--success)";
            authMessage.textContent = data?.mensagem || "Usuário criado com sucesso";
            // opcional: voltar para login automaticamente
            setTimeout(() => {
                btnShowLogin.click();
                authMessage.textContent = "";
            }, 900);
        } catch (err) {
            authMessage.style.color = "var(--danger)";
            authMessage.textContent = err.message;
        }
    });

}// ---------- Dashboard logic ----------
    if (document.getElementById("btn-logout")) {
        // redirect to login if no token
        if (!localStorage.getItem("access_token")) {
            window.location.href = "index.html";
        }

        // elements
        const btnLogout = document.getElementById("btn-logout");
        const currentUserSpan = document.getElementById("current-user");
        const sideBtns = document.querySelectorAll(".side-btn");
        const sections = document.querySelectorAll(".section");

        // simple function to decode JWT payload (not secure, only to read fields)
        function parseJwt(token) {
            try {
                const payload = token.split(".")[1];
                return JSON.parse(decodeURIComponent(atob(payload).split('').map(function (c) {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }).join('')));
            } catch {
                return null;
            }
        }

        // show current user id (we don't have username in token, but show sub)
        const token = localStorage.getItem("access_token");
        const payload = parseJwt(token);
        if (payload) {
            currentUserSpan.textContent = `User: ${payload.sub}`;
        }

        btnLogout.addEventListener("click", () => {
            localStorage.removeItem("access_token");
            window.location.href = "index.html";
        });

        // sidebar navigation
        sideBtns.forEach((b) => {
            b.addEventListener("click", () => {
                sideBtns.forEach(x => x.classList.remove("active"));
                b.classList.add("active");
                const sectionId = b.dataset.section;
                sections.forEach(s => s.classList.remove("active"));
                document.getElementById(sectionId).classList.add("active");
            });
        });

        // ---------- Equipments ----------
        const equipmentTableBody = document.querySelector("#equipment-table tbody");
        const equipmentMsg = document.getElementById("equipment-message");
        const equipmentForm = document.getElementById("equipment-form");
        document.getElementById("btn-add-equipment").addEventListener("click", () => {
            equipmentForm.classList.remove("hidden");
            document.getElementById("equipment-id").value = "";
            document.getElementById("equipment-name").value = "";
            document.getElementById("equipment-desc").value = "";
        });
        document.getElementById("cancel-equipment").addEventListener("click", () => {
            equipmentForm.classList.add("hidden");
        });
        document.getElementById("save-equipment").addEventListener("click", async () => {
            try {
                equipmentMsg.textContent = "";
                const id = document.getElementById("equipment-id").value;
                const name = document.getElementById("equipment-name").value.trim();
                const description = document.getElementById("equipment-desc").value.trim();
                if (!name) { equipmentMsg.textContent = "Nome obrigatório"; return; }
                if (id) {
                    // PUT
                    const res = await request(`/equipment/${id}`, {
                        method: "PUT",
                        body: JSON.stringify({ name, description })
                    });
                } else {
                    const res = await request(`/equipment/`, {
                        method: "POST",
                        body: JSON.stringify({ name, description })
                    });
                }
                equipmentForm.classList.add("hidden");
                loadEquipments();
            } catch (err) {
                equipmentMsg.textContent = err.message;
            }
        });

        async function loadEquipments() {
            equipmentTableBody.innerHTML = "<tr><td colspan='4'>Carregando...</td></tr>";
            try {
                const data = await request("/equipment");
                const list = data?.equipment || [];
                if (!list.length) {
                    equipmentTableBody.innerHTML = "<tr><td colspan='4'>Nenhum equipamento encontrado</td></tr>";
                    return;
                }
                equipmentTableBody.innerHTML = "";
                list.forEach(e => {
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
          <td>${e.id}</td>
          <td>${e.name || "-"}</td>
          <td>${e.description || "-"}</td>
          <td>
            <button class="secondary small" data-id="${e.id}" data-action="edit">Editar</button>
            <button class="secondary small" data-id="${e.id}" data-action="delete">Deletar</button>
          </td>
        `;
                    equipmentTableBody.appendChild(tr);
                });
            } catch (err) {
                equipmentTableBody.innerHTML = `<tr><td colspan='4'>Erro: ${err.message}</td></tr>`;
            }
        }

        equipmentTableBody.addEventListener("click", async (ev) => {
            const btn = ev.target.closest("button");
            if (!btn) return;
            const id = btn.dataset.id;
            const action = btn.dataset.action;
            if (action === "edit") {
                try {
                    const data = await request(`/equipment/${id}`);
                    document.getElementById("equipment-id").value = data.id;
                    document.getElementById("equipment-name").value = data.name || "";
                    document.getElementById("equipment-desc").value = data.description || "";
                    equipmentForm.classList.remove("hidden");
                } catch (err) {
                    equipmentMsg.textContent = err.message;
                }
            } else if (action === "delete") {
                if (!confirm("Confirma exclusão?")) return;
                try {
                    await request(`/equipment/${id}`, { method: "DELETE" });
                    loadEquipments();
                } catch (err) {
                    equipmentMsg.textContent = err.message;
                }
            }
        });

        // ---------- Equipment Safety ----------
        const equipmentSafetyTableBody = document.querySelector("#equipmentSafety-table tbody");
        const equipmentSafetyMsg = document.getElementById("equipmentSafety-message");
        const equipmentSafetyForm = document.getElementById("equipmentSafety-form");

        document.getElementById("btn-add-equipmentSafety").addEventListener("click", () => {
            equipmentSafetyForm.classList.remove("hidden");
            document.getElementById("equipmentSafety-id").value = "";
            document.getElementById("equipmentSafety-name").value = "";
            document.getElementById("equipmentSafety-desc").value = "";
        });
        document.getElementById("cancel-equipmentSafety").addEventListener("click", () => {
            equipmentSafetyForm.classList.add("hidden");
        });
        document.getElementById("save-equipmentSafety").addEventListener("click", async () => {
            try {
                equipmentSafetyMsg.textContent = "";
                const id = document.getElementById("equipmentSafety-id").value;
                const name = document.getElementById("equipmentSafety-name").value.trim();
                const description = document.getElementById("equipmentSafety-desc").value.trim();
                if (!name) { equipmentSafetyMsg.textContent = "Nome obrigatório"; return; }
                if (id) {
                    const res = await request(`/equipment-safety/${id}`, {
                        method: "PUT",
                        body: JSON.stringify({ name, description })
                    });
                } else {
                    const res = await request(`/equipment-safety/`, {
                        method: "POST",
                        body: JSON.stringify({ name, description })
                    });
                }
                equipmentSafetyForm.classList.add("hidden");
                loadEquipmentSafety();
            } catch (err) {
                equipmentSafetyMsg.textContent = err.message;
            }
        });

        async function loadEquipmentSafety() {
            equipmentSafetyTableBody.innerHTML = "<tr><td colspan='4'>Carregando...</td></tr>";
            try {
                const data = await request("/equipment-safety");
                const list = data?.equipmentSafety || [];
                if (!list.length) {
                    equipmentSafetyTableBody.innerHTML = "<tr><td colspan='4'>Nenhum item encontrado</td></tr>";
                    return;
                }
                equipmentSafetyTableBody.innerHTML = "";
                list.forEach(e => {
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
          <td>${e.id}</td>
          <td>${e.name || "-"}</td>
          <td>${e.description || "-"}</td>
          <td>
            <button class="secondary small" data-id="${e.id}" data-action="edit">Editar</button>
            <button class="secondary small" data-id="${e.id}" data-action="delete">Deletar</button>
          </td>
        `;
                    equipmentSafetyTableBody.appendChild(tr);
                });
            } catch (err) {
                equipmentSafetyTableBody.innerHTML = `<tr><td colspan='4'>Erro: ${err.message}</td></tr>`;
            }
        }

        equipmentSafetyTableBody.addEventListener("click", async (ev) => {
            const btn = ev.target.closest("button");
            if (!btn) return;
            const id = btn.dataset.id;
            const action = btn.dataset.action;
            if (action === "edit") {
                try {
                    const data = await request(`/equipment-safety/${id}`);
                    document.getElementById("equipmentSafety-id").value = data.id;
                    document.getElementById("equipmentSafety-name").value = data.name || "";
                    document.getElementById("equipmentSafety-desc").value = data.description || "";
                    equipmentSafetyForm.classList.remove("hidden");
                } catch (err) {
                    equipmentSafetyMsg.textContent = err.message;
                }
            } else if (action === "delete") {
                if (!confirm("Confirma exclusão?")) return;
                try {
                    await request(`/equipment-safety/${id}`, { method: "DELETE" });
                    loadEquipmentSafety();
                } catch (err) {
                    equipmentSafetyMsg.textContent = err.message;
                }
            }
        });

        // ---------- Vehicles ----------
        const vehicleTableBody = document.querySelector("#vehicle-table tbody");
        const vehicleMsg = document.getElementById("vehicle-message");
        const vehicleForm = document.getElementById("vehicle-form");

        document.getElementById("btn-add-vehicle").addEventListener("click", () => {
            vehicleForm.classList.remove("hidden");
            document.getElementById("vehicle-id").value = "";
            document.getElementById("vehicle-type").value = "";
            document.getElementById("vehicle-model").value = "";
            document.getElementById("vehicle-year").value = "";
        });
        document.getElementById("cancel-vehicle").addEventListener("click", () => {
            vehicleForm.classList.add("hidden");
        });
        document.getElementById("save-vehicle").addEventListener("click", async () => {
            try {
                vehicleMsg.textContent = "";
                const id = document.getElementById("vehicle-id").value;
                const type = document.getElementById("vehicle-type").value.trim();
                const model = document.getElementById("vehicle-model").value.trim();
                const year = parseInt(document.getElementById("vehicle-year").value);
                if (!type || !model || !year) { vehicleMsg.textContent = "Preencha todos os campos"; return; }
                if (id) {
                    const res = await request(`/vehicles/${id}`, {
                        method: "PUT",
                        body: JSON.stringify({ type, model, year })
                    });
                } else {
                    const res = await request(`/vehicles/`, {
                        method: "POST",
                        body: JSON.stringify({ type, model, year })
                    });
                }
                vehicleForm.classList.add("hidden");
                loadVehicles();
            } catch (err) {
                vehicleMsg.textContent = err.message;
            }
        });

        async function loadVehicles() {
            vehicleTableBody.innerHTML = "<tr><td colspan='5'>Carregando...</td></tr>";
            try {
                const data = await request("/vehicles");
                const list = data?.vehicle || [];
                if (!list.length) {
                    vehicleTableBody.innerHTML = "<tr><td colspan='5'>Nenhum veículo encontrado</td></tr>";
                    return;
                }
                vehicleTableBody.innerHTML = "";
                list.forEach(v => {
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
          <td>${v.id}</td>
          <td>${v.type || "-"}</td>
          <td>${v.model || "-"}</td>
          <td>${v.year || "-"}</td>
          <td>
            <button class="secondary small" data-id="${v.id}" data-action="edit">Editar</button>
            <button class="secondary small" data-id="${v.id}" data-action="delete">Deletar</button>
          </td>
        `;
                    vehicleTableBody.appendChild(tr);
                });
            } catch (err) {
                vehicleTableBody.innerHTML = `<tr><td colspan='5'>Erro: ${err.message}</td></tr>`;
            }
        }

        vehicleTableBody.addEventListener("click", async (ev) => {
            const btn = ev.target.closest("button");
            if (!btn) return;
            const id = btn.dataset.id;
            const action = btn.dataset.action;
            if (action === "edit") {
                try {
                    const data = await request(`/vehicles/${id}`);
                    document.getElementById("vehicle-id").value = data.id;
                    document.getElementById("vehicle-type").value = data.type || "";
                    document.getElementById("vehicle-model").value = data.model || "";
                    document.getElementById("vehicle-year").value = data.year || "";
                    vehicleForm.classList.remove("hidden");
                } catch (err) {
                    vehicleMsg.textContent = err.message;
                }
            } else if (action === "delete") {
                if (!confirm("Confirma exclusão?")) return;
                try {
                    await request(`/vehicles/${id}`, { method: "DELETE" });
                    loadVehicles();
                } catch (err) {
                    vehicleMsg.textContent = err.message;
                }
            }
        });

        // ---------- inicializa dados ----------
        (function initAll() {
            loadEquipments();
            loadEquipmentSafety();
            loadVehicles();
        })();
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('hidden'));
    }

    

