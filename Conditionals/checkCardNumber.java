boolean checkCardNumber(String cardNumber) 
{
	int lengthOfCardNumber = cardNumber.length();
    boolean flag = true;
    char[] charArray = cardNumber.toCharArray();
    
    //checking if all the characters are numbers
    for (char elt : charArray) {
        if (!Character.isDigit(elt)) {
            return false;
        }
    }
    

    //checking length of the card
    if ((lengthOfCardNumber == 14) || ((lengthOfCardNumber < 13) || (lengthOfCardNumber > 19))) {
            return false;
    }
    
    //Check according to the first numbers of the card number
    if (cardNumber.charAt(0) != '4') {
        if ((!cardNumber.startsWith("34")) && (!cardNumber.startsWith("37"))) {
            int firstTwoCharsIntegers = Integer.valueOf(cardNumber.substring(0,2));
            int firstFourCharsIntegers = Integer.valueOf(cardNumber.substring(0,4));
            if ((firstTwoCharsIntegers < 51) || (firstTwoCharsIntegers > 55)) {
                if ((firstFourCharsIntegers < 2221) || (firstFourCharsIntegers > 2720)) {
                    if (firstTwoCharsIntegers != 62) {
                        flag = false;
                    }
                }
            }
        }
    }
    
    //Luhn algorithm
    int i = lengthOfCardNumber-1;
    int sumOfElements = 0;
    
    while (i>=0) {
	   	 int firstElement = Character.getNumericValue(charArray[i]);
	   	 
	   	 if (i!=0) {
		    	 int secondElement = Character.getNumericValue(charArray[i-1]);
		    	 secondElement *= 2;
		    	 if (secondElement > 9) {
		    		 secondElement -= 9;
		    	 }
		    	 sumOfElements += firstElement + secondElement;
		    	 
	   	 }
	   	 else {
	   		 sumOfElements += firstElement;
	   	 }
	   	 i = i-2;
    }
    
    if (!(sumOfElements % 10 == 0)) {
    	flag = false; 	
    }
    
    return flag;
}