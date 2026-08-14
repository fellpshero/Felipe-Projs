public class RelatoriosMedicos {
    public static void main(String[] args) {
        System.out.println("Hello World");
        //String[] medicos = new String[5];
        //int[][] pacientes = new int[5][3];
        //int[] pacsMedicos = new int[5];

        String[] medicos = {"Dr Fernando", "Dr Maria", "Dr Sonia", "Dr Pedro", "Dra Daiana"};
        int[][] pacientes = {
            {120, 135, 128},
            {98, 110, 105},
            {150, 142, 160},
            {85, 92, 88},
            {130, 125, 140},
        };

            for (int i=0; i <medicos.length; i++) { // i ++ é o mesmo que i = i + 1
                System.out.printf("%12s", medicos[i], " - Pacientes:");
                for (int[] j = 0; j < 3; j++) {}
                int[] totalMed = new int[5];
                totalMed[i] = 0;

                for (int j=0; j <pacientes[i].length; j++) {
                    System.out.printf("%5d   ", pacientes[i][j]);
                    totalMed[i] = totalMed[i] + pacientes[i][j];
                }
                System.out.printf("%5d %7.1f \n", totalMed[i], totalMed[i]/3.0);
                }
            }
        }