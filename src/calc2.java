import java.util.Scanner;

public class calc2 {
    public static void main(String[] args) {
        Scanner leitor = new Scanner(System.in);

        System.out.println("Digite o seu primeiro número:");
            double n1 = leitor.nextDouble();
        System.out.println("Digite a operação desejada:");
            String op = leitor.next();
        System.out.println("Digite o seu segundo número:");
            double n2 = leitor.nextDouble();

    switch (op) {
        case "+":
            System.out.println("Resultado: " + (n1 + n2));
            break;
        case "-":
            System.out.println("Resultado: " + (n1 - n2));
            break;
        case "/":
            if (n2 == 0) {
                System.out.println("Ce é burro ne?");
            } else {
            System.out.println("Resultado: " + (n1 / n2));
            }
            break;
        case "*":
            System.out.println("Resultado: " + (n1 * n2));
            break;
        
    default:
        System.out.println("Operação inválida!");
        
        }
        leitor.close();
    }
}