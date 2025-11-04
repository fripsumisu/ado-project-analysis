import unittest

from src import ado_repo_analyser


class AdoRepoAnalyserTest(unittest.TestCase):

    def test_get_repo_stats(self):
        sample_repo = {
            'cloneUrl': 'https://myorg@dev.azure.com/my-org/my-project/_git/my-repo',
            'defaultBranch': 'refs/heads/develop',
            'name': 'my-repo',
            'repoId': 'd48cdc92-6b3c-486f-aa27-e635ea5ad617',
            'size': 19969047
        }
        updated_repo = ado_repo_analyser.get_repo_stats(ado_repo_summary=sample_repo)
        self.assertTrue('branches' in updated_repo, "No branches found for test repo")


if __name__ == '__main__':
    unittest.main()
