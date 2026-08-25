public class Main {
    public static void main(String[] args) {
        String especie[] = {"cao", "outro", "gato", "cao", "gato", "outro", "outro", "gato", "cao", "gato", "cao", "gato"};
        char doenca[] = {'n', 's', 'n', 'n', 'n', 'n', 's', 'n', 'n', 'n', 'n', 'n'};
        int idade[] = {61, 12, 70, 120, 6, 61, 36, 80, 180, 18, 81, 60};
        double peso[] = {9.2, 0.03, 4.0, 30.0, 2.5, 5.2, 0.15, 4.0, 20.0, 3.0, 11.5, 7.0};

        for (int i=0; i < especie.length;)
            if(especie[i].equalsIgnoreCase("cao")){
                if(peso[i] < 5){
                    System.out.println("Pequeno Porte");
                } else if (peso[i] < 20){
                    System.out.println("Médio Porte");
                } else {
                    System.out.println("Grande Porte");
                }
            }
        }
    }
