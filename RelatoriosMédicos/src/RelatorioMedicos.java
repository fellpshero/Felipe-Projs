public class RelatorioMedicos {
   public static void main(String[] args) {
       System.out.println("Hello, world");


       // 1. Ler o nome de cada médico (vetor de caractere)
       String[] medicos = {"Dr Fernando", "Dra Maria", "Dra Sonia", "Dr Pedro", "Dra Naiara"};


       // 2. Ler a quantidade de pacientes atendidos por mês (matriz inteira - 5 médicos × 3 meses)
       int[][] pacientes = {{120, 135, 128}, {98, 110, 105}, {150, 142, 160}, {85, 92, 88}, {130, 125, 140}};


       // 3. Calcular o total de pacientes atendidos por cada médico
       int[] totalMed = new int[5]; // Declara, aloca memória (operador new)
       // e inicializa todos os elementos com 0 por padrão.


       // 4. Calcular a média mensal de atendimentos de cada médico
       double[] totalMedMedia = new double[5];// Declara, aloca memória (operador new)
       // e inicializa todos os elementos com 0.0 por padrão.


       // 5. Exibir relatório completo: médico, total, média e status
       //• (bônus se média > 100: status = 'BÔNUS', senão status = "Regular"
       String[] status = new String[5];


       // 6. Informar o médico com maior número de atendimentos
       int maiorAtende = totalMed[0];
       String medicoMaior = medicos[0];


       // 7. Informar o total de pacientes atendidos pelo hospital
       int totalPac = 0;


       for (int i = 0; i < medicos.length; i++) { // i++ é o mesmo que i = i + 1
           totalMed[i] = 0; // Inicialização: primeira parte do padrão do acumulador.
           // Em Java esse comando é redundante.
            for (int j = 0; j < 3; j++) {
               totalMed[i] = totalMed[i] + pacientes[i][j];  // Acumulação: segunda parte do padrão do acumulador
           }


            totalMedMedia[i] = totalMed[i] / 3.0;
            if (totalMedMedia[i] > 100){
                status[i] = "BÔNUS";
            } else {
                status[i] = "Regular";
            }
            //logica calculo do maior
           if(totalMed[i] > maiorAtende){
               maiorAtende = totalMed[i];
               medicoMaior = medicos[i];


           }


            totalPac += totalMed[i]; // += é o mesmo de a = a+b -> a+=b, funciona como acumulador


       }


       for (int i = 0; i < medicos.length; i++) { // i++ é o mesmo que i = i + 1


           System.out.printf("%12s %5d %7.1f %9s\n", medicos[i], totalMed[i], totalMedMedia[i], status[i]);
       }
       System.out.println("Médico com maior número de atendimentos: " + medicoMaior);
       System.out.println("Dra Sonia - " + maiorAtende + " pacientes");
       System.out.println("Total de pacientes " + totalPac);


   }
}