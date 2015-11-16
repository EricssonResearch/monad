package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.util.concurrent.ExecutionException;

public class ForgotPasswordPopup extends AppCompatActivity {
    private EditText emailField;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_forgot_password);

        emailField = (EditText) findViewById(R.id.field_email);
        Button submitButton = (Button) findViewById(R.id.button_submit);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int) (width*.94),(int) (height*.30));

        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(emailField.getText().length() > 0
                        && emailField.getText().toString().contains("@")) {
                    SendResetPasswordRequest sendResetPasswordRequest = new SendResetPasswordRequest();
                    try {
                        String email = emailField.getText().toString();
                        //TODO: check email address exists and is not a google account (only) in the database
                        String response = sendResetPasswordRequest.execute(email).get();
                        //response is only the code now, nothing else
                        Toast.makeText(getApplicationContext(),
                                getString(R.string.java_forgotpassword_codesent),
                                Toast.LENGTH_LONG).show();
                        Intent intent = new Intent(v.getContext(), ConfirmCodePopup.class);
                        intent.putExtra("EMAIL", email);
                        intent.putExtra("CODE", response);
                        startActivity(intent);
                        finish();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } catch (ExecutionException e) {
                        e.printStackTrace();
                    }
                }
            }
        });
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
