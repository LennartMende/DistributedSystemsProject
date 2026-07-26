/*
mithilfe von Microsoft Copilot erstellt

*/

package com.mende.examination.soarms;

import javax.net.ssl.*;
import java.io.FileInputStream;
import java.security.KeyStore;
import java.security.cert.CertificateFactory;

public class SslUtil {

    public static SSLSocketFactory getSocketFactory(
            String truststorePath,
            String truststorePassword,
            String keystorePath,
            String keystorePassword
    ) throws Exception {

        // Truststore laden (CA)
        KeyStore trustStore = KeyStore.getInstance("PKCS12");
        System.out.println("Keystore path: " + keystorePath);
        System.out.println("Exists       : " + new java.io.File(keystorePath).exists());
        System.out.println("Absolute path: " + new java.io.File(keystorePath).getAbsolutePath());
        System.out.println("Password     : " + keystorePassword);

        System.out.println("Truststore: " + truststorePath);
        System.out.println("Exists: " + new java.io.File(truststorePath).exists());
        System.out.println("Absolute: " + new java.io.File(truststorePath).getAbsolutePath());
        try (FileInputStream ts = new FileInputStream(truststorePath)) {
            trustStore.load(ts, truststorePassword.toCharArray());
        }

        TrustManagerFactory tmf = TrustManagerFactory.getInstance(
                TrustManagerFactory.getDefaultAlgorithm()
        );
        tmf.init(trustStore);

        // Keystore laden (Client-Zertifikat)
        KeyStore keyStore = KeyStore.getInstance("PKCS12");
        try (FileInputStream ks = new FileInputStream(keystorePath)) {
            keyStore.load(ks, keystorePassword.toCharArray());
        }

        KeyManagerFactory kmf = KeyManagerFactory.getInstance(
                KeyManagerFactory.getDefaultAlgorithm()
        );
        kmf.init(keyStore, keystorePassword.toCharArray());

        // SSLContext bauen
        SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
        sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

        return sslContext.getSocketFactory();
    }
}
