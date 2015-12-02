package se.uu.csproject.monadclient.activities;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import se.uu.csproject.monadclient.R;

public class ConfirmCodePopup extends AppCompatActivity {

    private EditText confirmationCode;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_confirm_code);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int) (width*.94),(int) (height*.30));

        confirmationCode = (EditText) findViewById(R.id.field_code);
        Button submitButton = (Button) findViewById(R.id.button_submit);

        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //int codeValue = Integer.valueOf(confirmationCode.getText().toString());
                String codeValue = confirmationCode.getText().toString();

                Bundle extras = getIntent().getExtras();
                String rightCode = null;
                String email = null;

                if (extras != null) {
                    rightCode = extras.getString("CODE");
                    email = extras.getString("EMAIL");
                }

                if(codeValue.equals(rightCode)){
                    Intent intent = new Intent(ConfirmCodePopup.this, ResetPasswordActivity.class);
                    intent.putExtra("EMAIL", email);
                    intent.putExtra("RESET", true);
                    startActivity(intent);
                    finish();
                }
                else{
                    Toast.makeText(getApplicationContext(), getString(R.string.java_confirmcode_error), Toast.LENGTH_LONG).show();
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