// Classe que simula a Thread de Download
class DownloadThread extends Thread {
    @Override
    public void run() {
        System.out.println("[Download] Iniciando o download do arquivo grande...");
        
        try {
            // Simula o download de 10 partes do arquivo
            for (int i = 1; i <= 10; i++) {
                System.out.println("[Download] Baixando parte " + i + "0%...");
                
                // O sleep simula o tempo de rede. É aqui que o Java checa se houve interrupção.
                Thread.sleep(1000); 
            }
            System.out.println("[Download] Concluído com sucesso! 🎉");
            
        } catch (InterruptedException e) {
            // O bloco catch REAGE à interrupção (é a nossa rotina de tratamento)
            System.out.println("\n[INTERRUPÇÃO] O usuário clicou em Cancelar!");
            System.out.println("[Download] Limpando arquivos temporários corrompidos...");
            System.out.println("[Download] Processo abortado com segurança. ❌");
        }
    }
}

// Classe Principal para rodar o teste
public class ExJava {
    public static void main(String[] args) {
        // 1. Cria e inicia a thread do download
        DownloadThread download = new DownloadThread();
        download.start();

        // 2. O sistema principal espera 3 segundos (tempo do usuário pensar)
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // 3. O usuário decide "clicar no botão cancelar" -> Dispara a interrupção
        System.out.println("\n[Sistema] Botão 'Cancelar' foi pressionado!");
        download.interrupt(); 
    }
}