public class Main {
    public static void main(String[] args) {
        String especie[] = {"cao", "outro", "gato", "cao", "gato", "outro", "outro", "gato", "cao", "gato", "cao", "gato"};
        char doenca[] = {'n', 's', 'n', 'n', 'n', 'n', 's', 'n', 'n', 'n', 'n', 'n'};
        int idade[] = {61, 12, 70, 120, 6, 61, 36, 80, 180, 18, 81, 60};
        double peso[] = {9.2, 0.03, 4.0, 30.0, 2.5, 5.2, 0.15, 4.0, 20.0, 3.0, 11.5, 7.0};


        for (int i = 0; i < especie.length; i++) {
            if (especie[i].equalsIgnoreCase("cao")) {
                if (peso[i] < 5) {
                    System.out.println("Cão de Pequeno Porte");
                } else if (peso[i] < 20) {
                    System.out.println("Cão de Médio Porte");
                } else {
                    System.out.println("Cão de Grande Porte");
                }
            }
        }

        System.out.println("\nMédias de idade e peso");
        int somaIdade = 0;
        double somaPeso = 0;
        for(int i=0; i<especie.length; i++){
            somaIdade = somaIdade + idade[i];
            somaPeso = somaPeso + peso[i];
        }
        double mediaIdade = (double) somaIdade/especie.length;
        double mediaPeso = somaPeso/especie.length;
        System.out.printf("Média de idade: %.2f\n", mediaIdade);
        System.out.printf("Média de peso: %.2f\n", mediaPeso);
    }
}