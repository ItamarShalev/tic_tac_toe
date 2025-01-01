document.querySelectorAll('.cell').forEach(cell => {
    cell.addEventListener('click', () => {
        const cellIndex = cell.getAttribute('data-cell');
        window.location.href = `/move/${cellIndex}`;
    });
});
