package se.uu.csproject.monadclient.activities;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.concurrent.ExecutionException;

import se.uu.csproject.monadclient.serverinteractions.ClientAuthentication;
import se.uu.csproject.monadclient.R;

public class ResetPasswordActivity extends MenuedActivity {

    private EditText passwordField;
    private EditText confirmPasswordField;
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
        Button submitButton = (Button) findViewById(R.id.button_reset);
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

        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String passwordValue = passwordField.getText().toString();
                String confirmPasswordValue = confirmPasswordField.getText().toString();

                if (!passwordValue.equals(confirmPasswordValue)) {
                    Toast.makeText(getApplicationContext(), getString(R.string.java_passwordsnomatch), Toast.LENGTH_LONG).show();
                    return;
                }

                if (resetMode) {
                    Bundle extras = getIntent().getExtras();
                    String email = null;

                    if (extras != null) {
                        email = extras.getString("EMAIL");
                    }

                    ResetPasswordTask task = new ResetPasswordTask();

                    String response = null;
                    try {
                        response = task.execute(email, passwordValue).get();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } catch (ExecutionException e) {
                        e.printStackTrace();
                    }

                    if (response.startsWith("Success (1)")) {
                        Toast.makeText(getApplicationContext(), getString(R.string.java_pswd_resetsuccess), Toast.LENGTH_LONG).show();
                        finish();
                    } else {
                        Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
                    }
                } else {
                    String oldPassword = oldPasswordField.getText().toString();

                    UpdatePasswordTask task = new UpdatePasswordTask();

                    String response = null;
                    try {
                        response = task.execute(ClientAuthentication.getClientId(), oldPassword, passwordValue).get();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } catch (ExecutionException e) {
                        e.printStackTrace();
                    }

                    if (response.startsWith("Success (1)")) {
                        Toast.makeText(getApplicationContext(), getString(R.string.java_pswd_updatesuccess), Toast.LENGTH_LONG).show();
                        finish();
                    } else {
                        Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
                    }
                }
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        if(!resetMode){
            super.onCreateOptionsMenu(menu);
        }
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        return id == R.id.action_settings || super.onOptionsItemSelected(item);

    }

    private class ResetPasswordTask extends AsyncTask<String, Void, String>{

        @Override
        protected String doInBackground(String... params) {
            String response = ClientAuthentication.postForgottenPasswordResetRequest(params[0], params[1]);

            return response;
        }
    }

    private class UpdatePasswordTask extends AsyncTask<String, Void, String>{

        @Override
        protected String doInBackground(String... params) {
            String response = ClientAuthentication.postExistingPasswordUpdateRequest(params[0], params[1], params[2]);

            return response;
        }
    }
}
