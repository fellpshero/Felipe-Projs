import java.util.Scanner; // classe para ler dados do teclado no console
public class Main {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);  // lê dados do teclado
        // System.out.println("digite");
        // int teste = scan.nextInt();

        String especie[] = {"cao", "outro", "gato", "cao", "gato", "outro", "outro",
                "gato", "cao", "gato", "cao", "gato"};
        char doenca[] = {'n', 's', 'n', 'n', 'n', 'n', 's', 'n', 'n', 'n', 'n', 'n'};
        int idade[] = {61, 12, 70, 120, 6, 61, 36, 80, 180, 18, 81, 60};
        double peso[] = {9.2, 0.03, 4.0, 30.0, 2.5, 5.2, 0.15, 4.0, 20.0, 3.0, 11.5, 7.0};

        //     Exibir os dados como uma tabela
        for (int i = 0; i < especie.length; i++) {
            System.out.printf("%10s %10c %10d %10.2f\n", especie[i], doenca[i], idade[i], peso[i]);
        }

        /*
        1) Classificar os cães segundo a tabela:
        Até 5 kg Cão de porte pequeno
        Acima de 5 kg até 20 kg Cão de porte médio
        Acima de 20 kg Cão de porte grande
         */
        // Usar o campo length em vez de escrever o tamanho explicitamente
        System.out.println("\n Classificação do porte de cães");
        for (int i = 0; i < especie.length; i++) {
            if (especie[i].equalsIgnoreCase("cao")) {
                if (peso[i] < 5) {
                    System.out.println("port pequeno");
                } else if (peso[i] < 20) {
                    System.out.println("porte médio");
                } else {
                    System.out.println("porte grande");
                }
            }
        }

        System.out.println("\nMédias de idade e peso");
        int somaIdade = 0;
        double somaPeso = 0;
        for (int i = 0; i < especie.length; i++) {
            somaIdade = somaIdade + idade[i];   // somaIdade += idade[i]
            somaPeso = somaPeso + peso[i];
        }
        double mediaIdade = (double) somaIdade / especie.length;
        /* operador de divisão inteira
        C, C++, Java, Go, Rust, Ruby, Kotlin: /
        Python, Lua: //
        VBA: \
        JavaScript Math.floor(i/j)
        PHP: intdiv(i,j)
        1) Distribuir itens em grupos: tem 47 alunos e quero formar turmas de 10:
        quantidade de turmas cheiasm: 47 / 10 = 4
        resto (47 % 10 = 7) diz quantos alunos sobram.

        2) Conversão entre unidades
        int totalSegundos = 3725;
        int horas = totalSegundos / 3600;
        int minutos = (totalSegundos % 3600) / 60;
        int segundos = totalSegundos % 60;

        3) Algoritmos
        Busca binária usa (inicio + fim) / 2 para achar o meio de um array.
        Conversão de base numérica (decimal → binário, por exemplo) é feita dividindo repetidamente por 2 e guardando os restos.
        */
        double mediaPeso = somaPeso / especie.length;
        System.out.printf("Média idade: %.2f\n", mediaIdade);
        System.out.printf("Média peso: %.2f\n", mediaPeso);

        System.out.println("\nMédia de peso dos gatos acima de 5 anos");
        double somaPesoGato60 = 0;
        int contGato60 = 0;
        for (int i = 0; i < especie.length; i++) {
            if (especie[i].equalsIgnoreCase("gato") && idade[i] > 60) {
                somaPesoGato60 += peso[i];
                contGato60++;
            }
        }
        double mediaPesoGato60 = somaPesoGato60 / contGato60;
        System.out.printf("Média: %.1f\n", mediaPesoGato60);

        System.out.print("  % not equals cão e gato  ");
        int contOutros =0;
        for (int i = 0; i < especie.length; i++) {
            if ( ! especie[i].equalsIgnoreCase("cao") &&
                  !  especie[i].equalsIgnoreCase("gato") ) {
                contOutros++; // contOutros = contOutros + 1;
            }
        }
        double percOutros = (double) contOutros / especie.length * 100;
        System.out.println(percOutros);

        // 8) Solicite que o usuário digite uma espécie e exiba os dados dos animais da espécie digitada.
        String especDig;
        System.out.println("\nDigite a espécie");
        especDig = scan.next(); // leia(especDig) só para String

        int achou = 0;
        for(int i=0; i<especie.length; i++){
            // if(especDig.equalsIgnoreCase(especie[i]))
            if(especie[i].equalsIgnoreCase(especDig)){
                System.out.printf("%10s %10c %10d %10.2f\n", especie[i],
                        doenca[i], idade[i], peso[i]);
                achou = 1;
            }
        }
        if(achou == 0) {
            System.out.println("Nenhum " + especDig + " encontrado.");
        }
    }
}
