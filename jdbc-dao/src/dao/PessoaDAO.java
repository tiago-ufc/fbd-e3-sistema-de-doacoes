package dao;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import model.Pessoa;
import util.DatabaseConnection;

public class PessoaDAO implements PessoaDAOI{
	
	DatabaseConnection db;

	@Override
	public Pessoa get(String email) {
		
		try {
			db = new DatabaseConnection();
			String sql = "select nome, email from pessoa where email=?";
			PreparedStatement st = db.getConnection().prepareStatement(sql);
			st.setString(1, email);
			ResultSet res = st.executeQuery();
			if(res.next()) {
				Pessoa p = new Pessoa();
				p.setNome(res.getString("nome"));
				p.setEmail(res.getString("email"));
				return p;
			}
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return null;
	}

	@Override
	public List<Pessoa> getAll() {
		try {
			db = new DatabaseConnection();
			String sql = "select nome, email from pessoa";
			Statement st = db.getConnection().createStatement();
			ResultSet res = st.executeQuery(sql);
			List<Pessoa> pessoasList = new ArrayList<Pessoa>();
			while(res.next()) {
				Pessoa p = new Pessoa();
				p.setNome(res.getString("nome"));
				p.setEmail(res.getString("email"));
				pessoasList.add(p);
			}
			return pessoasList;
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return null;
	}

	@Override
	public void save(Pessoa newp) {
		
		try {
			db = new DatabaseConnection();
			String sql = "insert into pessoa values(?,?)";
			PreparedStatement st;
			st = db.getConnection().prepareStatement(sql);
			st.setString(1, newp.getNome());
			st.setString(2, newp.getEmail());
			st.execute();

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}

	@Override
	public void update(Pessoa newp, Pessoa oldp) {
		try {
			db = new DatabaseConnection();
			String sql = "update pessoa set nome=?, email=? where email=?";
			PreparedStatement st;
			st = db.getConnection().prepareStatement(sql);
			st.setString(1, newp.getNome());
			st.setString(2, newp.getEmail());
			st.setString(3, oldp.getEmail());
			st.execute();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

	@Override
	public void delete(String email) {
		try {
			db = new DatabaseConnection();
			String sql = "delete from pessoa where email=?";
			PreparedStatement st;
			st = db.getConnection().prepareStatement(sql);
			st.setString(1, email);
			st.execute();

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	public static void main(String[] args) {
		PessoaDAO pessoaDao = new PessoaDAO();
		//Pessoa p = new Pessoa("Livia", "livia@gmail");
		//pessoaDao.save(p);
		// Pessoa p2 = pessoaDao.get("livia@gmail");
		// System.out.println(p2.getNome());
		// System.out.println(p2.getEmail());
		//Pessoa oldp = new Pessoa("Cristina", "cristina@gmail.com");
		//Pessoa newp = new Pessoa("Cristina Santos", "cristina@gmail.com");

		//pessoaDao.update(newp, oldp);
		pessoaDao.delete("livia@gmail");
		
		List<Pessoa> allPessoas = pessoaDao.getAll();
		for(int i = 0; i < allPessoas.size(); i++) {
			Pessoa p = allPessoas.get(i);
			System.out.println(p.getNome());
			System.out.println(p.getEmail());
		}
		
		try {
			pessoaDao.db.getConnection().close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}

}
