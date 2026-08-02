function initTablePagination(table, pageSize = 10) {
    const tbody = table.querySelector('tbody');
    if (!tbody) return;

    const rows = Array.from(tbody.querySelectorAll('tr:not(.pagination-row)'));
    const groups = [];
    const groupMap = new Map();

    rows.forEach(row => {
        const key = row.dataset.group ?? `single-${groups.length}`;
        if (!groupMap.has(key)) {
            groupMap.set(key, []);
            groups.push(groupMap.get(key));
        }
        groupMap.get(key).push(row);
    });

    if (groups.length <= pageSize) return;

    let shown = pageSize;

    function render() {
        groups.forEach((groupRows, index) => {
            const visible = index < shown;
            groupRows.forEach(row => {
                row.style.display = visible ? '' : 'none';
            });
        });

        let btnRow = tbody.querySelector('.pagination-row');
        const remaining = groups.length - shown;

        if (remaining <= 0) {
            if (btnRow) btnRow.remove();
            return;
        }

        if (!btnRow) {
            btnRow = document.createElement('tr');
            btnRow.className = 'pagination-row';

            const td = document.createElement('td');
            td.colSpan = table.querySelectorAll('thead th').length;

            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn-submit';
            btn.addEventListener('click', () => {
                shown += pageSize;
                render();
            });

            td.appendChild(btn);
            btnRow.appendChild(td);
            tbody.appendChild(btnRow);
        }

        const btn = btnRow.querySelector('.btn-submit');
        btn.innerHTML = `<i class="fas fa-chevron-down"></i> Ver mais (${remaining} restantes)`;
    }

    render();
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('table[data-paginate]').forEach(table => {
        const pageSize = parseInt(table.dataset.paginate, 10) || 10;
        initTablePagination(table, pageSize);
    });
});