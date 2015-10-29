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
            int ascii = (int) c;

//            if (ascii < 33 || ascii > 133)

        }
        return false;
    }

    public static boolean validateUsernameCharacter(Character c) {
//        Character[] invalid = {':', ',', '<', '>', '&', '', '', '', '', '', '', '', '', '', '', '', '', };
        return false;
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
}
