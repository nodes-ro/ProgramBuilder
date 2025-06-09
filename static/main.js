// event_program.js

document.addEventListener('DOMContentLoaded', () => {

    // 1) Auto-dismiss flash messages after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.flash-msg').forEach(msg => msg.remove());
    }, 5000);

    // 2) Download the schedule as HTML
    const downloadBtn = document.getElementById('download-schedule');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            const content = document.getElementById('export-section').innerHTML;
            const html = `
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <title>Exported Schedule</title>
            <link href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" rel="stylesheet">
          </head>
          <body>${content}</body>
        </html>`.trim();

            const blob = new Blob([html], {
                type: 'text/html'
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'schedule.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }

    // 3) Dynamic “Stage” dropdown
    const daySelect = document.getElementById('event-day');
    const stageSelect = document.getElementById('stage-select');
    if (daySelect && stageSelect) {
        daySelect.addEventListener('change', () => {
            const count = parseInt(daySelect.selectedOptions[0].dataset.stageCount, 10) || 0;
            stageSelect.innerHTML =
                '<option disabled selected value="">Select a stage</option>';
            for (let i = 1; i <= count; i++) {
                const opt = document.createElement('option');
                opt.value = i;
                opt.textContent = i;
                stageSelect.appendChild(opt);
            }
        });
    }

});

function toggleModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modal.open ? modal.close() : modal.showModal();
}