let timerInterval;
let seconds = 0;

export function showTimer() {
    document.getElementById('timerWindow').style.display = 'block';
    seconds = 0;
    timerInterval = setInterval(() => {
        seconds++;
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        document.getElementById('timerDisplay').textContent = 
            `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
    }, 1000);
}

export function hideTimer() {
    clearInterval(timerInterval);
    document.getElementById('timerWindow').style.display = 'none';
}

async function ejecutarSecuencia() {
    try {
        showTimer();
        const response = await fetch('/ejecutar_secuencia');
        const resultado = await response.text();
        const status = resultado.includes('❌') ? 'error' : 'success';
        showOutput(
            'Ejecución de Secuencia',
            resultado,
            'bi-play-circle-fill',
            status
        );
    } catch (error) {
        console.error('Error:', error);
        showOutput(
            'Error en la Ejecución',
            'Ha ocurrido un error al ejecutar la secuencia.',
            'bi-exclamation-triangle-fill',
            'error'
        );
    } finally {
        hideTimer();
    }
}

document.getElementById('ejecutarSecuenciaBtn').addEventListener('click', ejecutarSecuencia);