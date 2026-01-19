import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class ExemploConexao {
	
	public static void main(String[] args) {
		try {
			Class.forName("org.postgresql.Driver");
			String url = "jdbc:postgresql://localhost/empresa-fbd01";
			String user = "postgres";
			String password = "postgres";
			Connection con = DriverManager.getConnection(
					url,user,password);
			Statement st = con.createStatement();
			
			String sql = "update empresa.funcionario set unome=? where pnome=?";
			PreparedStatement pst = con.prepareStatement(sql);
			pst.setString(1,"Cruz");
			pst.setString(2, "Livia");
			int i = pst.executeUpdate();
			System.out.println(i);
				
			String sql2 = "delete from empresa.funcionario where pnome=?";
			pst = con.prepareStatement(sql2);
			pst.setString(1, "Livia");
			i = pst.executeUpdate();
			System.out.println(i);
			
			String sql3 = "insert into empresa.funcionario(cpf, pnome, minicial, unome, endereco) values (?,?,?,?,?)";
			pst = con.prepareStatement(sql3);
			pst.setString(1, "11122233355");
			pst.setString(2, "Barbara");
			pst.setString(3, "A");
			pst.setString(4, "Silva");
			pst.setString(5, "Rua x");
			i = pst.executeUpdate();
			System.out.println(i);
					
			
			ResultSet resultSet = st.executeQuery("select * from empresa.funcionario;");
			
			while(resultSet.next()) {
				System.out.println(resultSet.getString(1)+" "+resultSet.getString(3));
			}
			
			
			con.close();
			
		} catch (ClassNotFoundException | SQLException e) {
			e.printStackTrace();
		}
	}
}
