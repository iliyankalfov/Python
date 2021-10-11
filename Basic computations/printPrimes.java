void printPrimes(int max){
    for (int n=2;n<max;n++){
        boolean prime = true;
        for (int f=2;f<=Math.sqrt(n);f++){
            if (n%f==0)
            {
                prime=false;
                break;
            }
            
        }
        if (prime)
        {
            System.out.println(n+" is prime");
        }
    }
}