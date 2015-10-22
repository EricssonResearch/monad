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

import org.w3c.dom.Text;

public class ResetPasswordActivity extends AppCompatActivity {

    private EditText passwordField;
    private EditText confirmPasswordField;
    private Button resetButton;
    private Toolbar toolbar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_reset_password);

        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        passwordField = (EditText) findViewById(R.id.field_password);
        confirmPasswordField= (EditText) findViewById(R.id.field_verify_password);
        resetButton = (Button) findViewById(R.id.button_reset);

        //TODO: update the password in the database
        resetButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String passwordValue = passwordField.getText().toString();
                String confirmPasswordValue = confirmPasswordField.getText().toString();
                if(passwordValue.length() > 6 && passwordValue.equals(confirmPasswordValue)){
                    ResetPasswordActivity.this.startActivity(
                            new Intent(ResetPasswordActivity.this, LoginActivity.class));
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
