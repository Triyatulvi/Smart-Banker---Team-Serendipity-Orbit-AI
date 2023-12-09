document.getElementById("export-btn").addEventListener("click", function () {
  exportToCSV("data.csv");
});

function exportToCSV(filename) {
  var data = [];

  // Mengambil nilai dari formulir input
  var name_bank = document.getElementById("name_bank").value;
  var amount = document.getElementById("amount").value;
  var account_number = document.getElementById("account_number").value;
  var amount_debit = document.getElementById("amount_debit").value;

  // Memasukkan nilai ke dalam array data
  data.push(["Nama Bank", "Total kredit", "Nomor Rekening", "Total Debit"]); // Judul kolom
  data.push([name_bank, amount, account_number, amount_debit]); // Data pengguna

  // Membuat CSV
  var csvContent =
    "data:text/csv;charset=utf-8," + data.map((e) => e.join(",")).join("\n");

  // Membuat file CSV yang dapat diunduh
  var encodedUri = encodeURI(csvContent);
  var link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}


// var loadFile = function (event) {
//   var output = document.getElementById("output");
//   output.src = URL.createObjectURL(event.target.files[0]);
//   output.onload = function () {
//     URL.revokeObjectURL(output.src); // free memory
//   };
// };
