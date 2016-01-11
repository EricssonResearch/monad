package se.uu.csproject.monadvehicle.tools;

import java.security.MessageDigest;

/**
 *
 */
public class Security {

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
