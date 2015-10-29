package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

public class ResetPasswordActivity extends AppCompatActivity {

    private EditText passwordField;
    private EditText confirmPasswordField;
    private Button submitButton;
    private EditText oldPasswordField;
    private boolean resetMode;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_reset_password);

        Toolbar toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        passwordField = (EditText) findViewById(R.id.field_newpassword);
        confirmPasswordField= (EditText) findViewById(R.id.field_verify_password);
        submitButton = (Button) findViewById(R.id.button_reset);
        TextView resetPasswordText = (TextView) findViewById(R.id.label_resetpassword);
        TextView oldPasswordText = (TextView) findViewById(R.id.label_oldpassword);
        oldPasswordField = (EditText) findViewById(R.id.field_oldpassword);

        /* resetMode is true if this activity is accessed from ConfirmCodePopup
         * It is false if it is accessed from ProfileActivity,
         * In the second casem labels are changed and the current password textfield is visible
         */
        resetMode = getIntent().getExtras().getBoolean("RESET");
        if (!resetMode) {
            oldPasswordField.setVisibility(View.VISIBLE);
            oldPasswordText.setVisibility(View.VISIBLE);
            resetPasswordText.setText(getString(R.string.label_resetpassword_changepassword));
            submitButton.setText(getString(R.string.label_profile_savechanges));
        }

        //TODO: update the password in the database
        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String passwordValue = passwordField.getText().toString();
                String confirmPasswordValue = confirmPasswordField.getText().toString();

                if(passwordValue.length() < 6){
                    Toast.makeText(getApplicationContext(), "The password should contain at least 6 characters!", Toast.LENGTH_LONG).show();
                }
                else if(!passwordValue.equals(confirmPasswordValue)){
                    Toast.makeText(getApplicationContext(), "Two passwords do not match!", Toast.LENGTH_LONG).show();
                }

                if(resetMode){
                    Bundle extras = getIntent().getExtras();
                    String email = null;

                    if (extras != null) {
                        email = extras.getString("EMAIL");
                    }

                    String response = ClientAuthentication.postForgottenPasswordResetRequest(email, passwordValue);
                    Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
                    ResetPasswordActivity.this.startActivity(new Intent(ResetPasswordActivity.this, LoginActivity.class));
                }
                else {
                    String oldPassword = oldPasswordField.getText().toString();
                    String response = ClientAuthentication.postExistingPasswordUpdateRequest(ClientAuthentication.getClientId(), oldPassword, passwordValue);
                    Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
                    if(response.startsWith("Success (1)")) {
                        finish();
                    }
                }
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_login, menu);
        return true;
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
