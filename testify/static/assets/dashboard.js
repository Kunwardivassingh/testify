document.addEventListener('DOMContentLoaded', () => {
  fetchData();

  function fetchData() {
    fetch('/api/dashboard/data')
      .then(response => response.json())
      .then(data => {
        updateTable(data);
      })
      .catch(error => console.error('Error fetching data:', error));
  }

  function applyFilters() {
    const startDate = document.getElementById('date-range-start').value;
    const endDate = document.getElementById('date-range-end').value;
    const status = document.getElementById('status-filter').value;

    fetch(`/api/dashboard/data?start=${startDate}&end=${endDate}&status=${status}`)
      .then(response => response.json())
      .then(data => {
        updateTable(data);
      })
      .catch(error => console.error('Error applying filters:', error));
  }

  function updateTable(data) {
    const tbody = document.getElementById('data-body');
    tbody.innerHTML = '';
    data.forEach(row => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${row.id || '-'}</td>
        <td>${row.product_name || '-'}</td>
        <td>${row.test_type || '-'}</td>
        <td>${row.status || '-'}</td>
        <td>${row.execution_date || '-'}</td>
        <td>${row.tester || '-'}</td>
        <td>${row.test_duration || '-'}</td>
      `;
      tbody.appendChild(tr);
    });
  }
});