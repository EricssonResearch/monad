package se.uu.csproject.monadclient;

import java.security.MessageDigest;
import javax.mail.internet.AddressException;
import javax.mail.internet.InternetAddress;

/**
 *
 */
public class Security {

    public static boolean validateUsername(String username) {

        for (int i = 0; i < username.length(); i++) {
            Character c = username.charAt(i);

            if (!validateUsernameCharacter(c)) {
                return false;
            }

        }
        return true;
    }

    public static boolean isNumber(int ascii) {
        if (ascii > 47 && ascii < 58) {
            return true;
        }
        return false;
    }

    public static boolean isCapital(int ascii) {
        if (ascii > 64 && ascii < 91) {
            return true;
        }
        return false;
    }

    public static boolean isSmallCase(int ascii) {
        if (ascii > 96 && ascii < 123) {
            return true;
        }
        return false;
    }

    public static boolean validateUsernameCharacter(Character c) {
        int ascii = (int) c;

        if (isNumber(ascii) || isCapital(ascii) || isSmallCase(ascii)) {
            return true;
        }
        return false;
    }

    public static boolean validatePassword(String password){
        if(password.length() < 6) {
            return false;
        }
        else {
            return true;
        }
    }

    public static boolean validateEmail(String email) {

        try {
            InternetAddress internetAddress = new InternetAddress(email);
            internetAddress.validate();
            return true;
        }
        catch (AddressException e) {
            return false;
        }
    }

    public static boolean validatePhone(String phone) {

        for (int i = 0; i < phone.length(); i++) {
            Character c = phone.charAt(i);
            int ascii = (int) c;

            if (!isNumber(ascii) && (i > 0 || c != '+')) {
                return false;
            }
        }
        return true;
    }

    public static String encryptPassword(String password) {
        byte[] bytesOfPassword;
        byte[] bytesOfEncryptedPassword;
        String encryptedPassword = "";

        try {
            bytesOfPassword = password.getBytes("UTF-8");
            MessageDigest md = MessageDigest.getInstance("MD5");
            bytesOfEncryptedPassword = md.digest(bytesOfPassword);
            encryptedPassword = new String(bytesOfEncryptedPassword);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        return encryptedPassword;
    }

    public static String invalidUsernameMessage() {
        return "ERROR - Invalid username. Valid characters: (a-z, A-Z, 0-9)";
    }

    public static String invalidPasswordMessage(){
        return "ERROR - Password must have at least 6 characters";
    }

    public static String invalidEmailMessage() {
        return "ERROR - Invalid email address";
    }

    public static String invalidPhoneMessage() {
        return "ERROR - Phone number contains invalid characters";
    }
}
