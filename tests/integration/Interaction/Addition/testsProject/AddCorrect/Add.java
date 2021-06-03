import java.util.Scanner;

class Add{
    

    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);

        System.out.println("Entrez un premier entier");
        int a = sc.nextInt();
        System.out.println("Entrez un second entier");
        int b = sc.nextInt();
        System.out.println("La somme des deux nombres entrés est " + Integer.toString(a+b));
    } 
}