import java.util.Scanner;

public class Calc {
    public static void main(String[] args) {
    Scanner scan = new Scanner(System.in);
    
    System.out.println("Digite um número:");
        float n1 = scan.nextFloat();
    System.out.println("Qual a operação desejada?");
        String op = scan.next();
    System.out.println("Digite outro número:");
        float n2 = scan.nextFloat();

    switch (op) {
        case "+":
            System.out.println("Resultado: " + (n1 + n2));
            break;

        case "-":
            System.out.println("Resultado: " + (n1 - n2));
            break;

        case "/":
            if((n2 == 0)||(n1 == 0)){
                System.out.println("Não é possível dividir por zero!");
            } else {
            System.out.println("Resultado: " + (n1 / n2));}
            break;

        case "*":
            System.out.println("Resultado: " + (n1 * n2));
            break;

    default:
        System.out.println("Operação inválida!");
    }
    scan.close();
        }
    }