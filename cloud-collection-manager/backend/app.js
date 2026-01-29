const API = "https://YOUR-BACKEND-URL.onrender.com";

let currentPage = 1;

async function loadBooks() {
  const res = await fetch(`${API}/books?page=${currentPage}`);
  const data = await res.json();

  const container = document.getElementById("listView");
  container.innerHTML = "";

  const table = document.createElement("table");
  table.innerHTML = `
    <tr>
      <th>#</th>
      <th>Title</th>
      <th>Author</th>
      <th>Year</th>
      <th>Actions</th>
    </tr>
  `;

  data.books.forEach((b, i) => {
    table.innerHTML += `
      <tr>
        <td>${(currentPage - 1) * 10 + i + 1}</td>
        <td>${b.title}</td>
        <td>${b.author}</td>
        <td>${b.year}</td>
        <td>
          <button onclick="editBook(${b.id})">Edit</button>
          <button onclick="deleteBook(${b.id})">Delete</button>
        </td>
      </tr>
    `;
  });

  container.appendChild(table);
}

async function addBook() {
  const title = prompt("Title:");
  const author = prompt("Author:");
  const year = prompt("Year:");

  await fetch(`${API}/books`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, author, year })
  });

  loadBooks();
}

async function deleteBook(id) {
  if (!confirm("Delete this book?")) return;

  await fetch(`${API}/books/${id}`, { method: "DELETE" });
  loadBooks();
}

async function editBook(id) {
  const title = prompt("New title:");
  const author = prompt("New author:");
  const year = prompt("New year:");

  await fetch(`${API}/books/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, author, year })
  });

  loadBooks();
}

function nextPage() {
  currentPage++;
  loadBooks();
}

function prevPage() {
  if (currentPage > 1) currentPage--;
  loadBooks();
}

window.onload = loadBooks;
