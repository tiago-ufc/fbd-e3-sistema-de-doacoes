package dao;

import java.util.List;

import model.Pessoa;

public interface PessoaDAOI {
	Pessoa get(String email);
	List<Pessoa> getAll();
	void save(Pessoa newp);
	void update(Pessoa newp, Pessoa oldp);
	void delete(String email);
}
