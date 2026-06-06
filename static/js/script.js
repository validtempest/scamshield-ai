document.addEventListener(
    'DOMContentLoaded',
    () => {

        // ======================
        // ELEMENT SELECTORS
        // ======================

        const form =
            document.getElementById(
                'analyzeForm'
            );

        const button =
            document.getElementById(
                'analyzeBtn'
            );

        const input =
            document.getElementById(
                'messageInput'
            );

        const charCount =
            document.getElementById(
                'charCount'
            );

        const resultCard =
            document.querySelector(
                '.result-card'
            );

        const deleteForms = 
            document.querySelectorAll(
                '.delete-history-form'
            );

        // ======================
        // AUTO FOCUS INPUT
        // ======================

        if (input) {
            input.focus();
        }

        // ======================
        // CHARACTER COUNTER + LIMIT
        // ======================

        if (
            input &&
            charCount &&
            button
        ) {

            const MAX_LENGTH = 500;

            const updateCounter =
                () => {

                    const currentLength =
                        input.value.length;

                    charCount.textContent =
                        `${currentLength} / ${MAX_LENGTH}`;

                    // over limit
                    if (
                        currentLength >
                        MAX_LENGTH
                    ) {

                        charCount.style.color =
                            '#f43f5e'; /* rose color matching Tailwind */

                        button.disabled =
                            true;

                        button.innerHTML =
                            '<i class="fa-solid fa-ban mr-2"></i> Batas Karakter Terlampaui';

                    } else {

                        charCount.style.color =
                            '#94a3b8'; /* slate-400 matching Tailwind placeholder */

                        button.disabled =
                            false;

                        button.innerHTML =
                            '<i class="fa-solid fa-bolt mr-2"></i> Analisis Pesan';
                    }
                };

            updateCounter();

            input.addEventListener(
                'input',
                updateCounter
            );
        }

        // ======================
        // LOADING BUTTON & PROGRESS SCANNING EFFECT
        // ======================

        if (
            form &&
            button
        ) {

            form.addEventListener(
                'submit',
                () => {

                    button.disabled =
                        true;

                    // Insert scanner beam effect into card parent if exists
                    const card = form.closest('.glass-card');
                    if (card) {
                        const beam = document.createElement('div');
                        beam.className = 'scanner-beam';
                        card.classList.add('scanner-container');
                        card.appendChild(beam);
                    }

                    button.innerHTML =
                        `
                        <span class="ai-spinner mr-2"></span>
                        Pemindaian Pola AI...
                        `;
                }
            );
        }

        // ======================
        // RESULT CARD FADE-IN ANIMATION
        // ======================

        if (resultCard) {

            resultCard.style.opacity =
                '0';

            resultCard.style.transform =
                'translateY(20px)';

            resultCard.style.transition =
                'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';

            setTimeout(
                () => {

                    resultCard.style.opacity =
                        '1';

                    resultCard.style.transform =
                        'translateY(0)';
                },
                50
            );
        }

        // ======================
        // DYNAMIC METER PROGRESS
        // ======================

        const confidenceBar = document.getElementById('confidenceBar');
        const riskBar = document.getElementById('riskBar');

        if (confidenceBar) {
            const targetWidth = confidenceBar.getAttribute('data-width') || '0';
            setTimeout(() => {
                confidenceBar.style.width = `${targetWidth}%`;
            }, 150);
        }

        if (riskBar) {
            const targetWidth = riskBar.getAttribute('data-width') || '0';
            setTimeout(() => {
                riskBar.style.width = `${targetWidth}%`;
            }, 150);
        }

        // ======================
        // DELETE HISTORY VAULT SECURE CONFIRMATION
        // ======================

        if (deleteForms) {
            deleteForms.forEach(item => {
                item.addEventListener('submit', (event) => {
                    const confirmDeletion = confirm("Peringatan: Apakah Anda benar-benar yakin ingin menghapus data pemindaian ini secara permanen dari registri SQLite? Tindakan ini tidak dapat dibatalkan.");
                    if (!confirmDeletion) {
                        event.preventDefault();
                    }
                });
            });
        }

        // ======================
        // CLEAR ALL HISTORY SECURE CONFIRMATION
        // ======================

        const clearAllForm = document.getElementById('clearAllForm');
        if (clearAllForm) {
            clearAllForm.addEventListener('submit', (event) => {
                const confirmClear = confirm("Peringatan Kritis: Apakah Anda benar-benar yakin ingin menghapus SELURUH riwayat pemindaian dari database? Semua data telemetri akan hilang secara permanen!");
                if (!confirmClear) {
                    event.preventDefault();
                }
            });
        }
    }
);