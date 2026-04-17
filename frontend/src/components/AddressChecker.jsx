import { useState } from 'react';
import styled from 'styled-components';
import apiClient from '../services/apiClient';

const Container = styled.div`
  min-height: 100vh;
  background: #f5f5f5;
  padding: 40px 20px;
`;

const Content = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const Header = styled.div`
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
`;

const Title = styled.h1`
  color: #333;
  margin-bottom: 10px;
`;

const Subtitle = styled.p`
  color: #666;
  font-size: 14px;
`;

const Form = styled.form`
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 16px;
  font-family: inherit;
  transition: border-color 0.3s;

  &:focus {
    outline: none;
    border-color: #667eea;
  }
`;

const Button = styled.button`
  padding: 12px 30px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;

  &:hover {
    background: #5568d3;
  }

  &:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
`;

const ResultContainer = styled.div`
  margin-top: 30px;
  padding: 20px;
  border-radius: 5px;
  background: ${(props) => (props.valid ? '#e8f5e9' : '#ffebee')};
  border: 2px solid ${(props) => (props.valid ? '#4caf50' : '#d32f2f')};
`;

const ResultTitle = styled.h3`
  color: ${(props) => (props.valid ? '#2e7d32' : '#c62828')};
  margin-bottom: 10px;
`;

const ResultText = styled.p`
  color: #333;
  font-size: 14px;
`;

const ErrorMessage = styled.div`
  color: #d32f2f;
  background: #ffebee;
  padding: 12px;
  border-radius: 5px;
  margin-bottom: 20px;
  font-size: 14px;
`;

const LoadingText = styled.p`
  color: #667eea;
  font-weight: 500;
`;

const AddressChecker = () => {
  const [address, setAddress] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);

    if (!address.trim()) {
      setError('Please enter an address');
      return;
    }

    setLoading(true);
    try {
      const response = await apiClient.post('/validate-address', { address });
      setResult(response);
    } catch (err) {
      setError(err.message || 'Validation failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Content>
        <Header>
          <Title>Address Validator</Title>
          <Subtitle>Validate New Zealand addresses</Subtitle>
        </Header>

        <Form onSubmit={handleSubmit}>
          {error && <ErrorMessage>{error}</ErrorMessage>}

          <FormGroup>
            <Label htmlFor="address">Enter Address</Label>
            <TextArea
              id="address"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              placeholder="e.g., Queen Street, Auckland"
              rows="4"
              disabled={loading}
            />
          </FormGroup>

          <Button type="submit" disabled={loading}>
            {loading ? 'Validating...' : 'Validate Address'}
          </Button>

          {loading && <LoadingText style={{ marginTop: '20px' }}>Processing your request...</LoadingText>}
        </Form>

        {result && (
          <ResultContainer valid={result.status === 'valid'}>
            <ResultTitle valid={result.status === 'valid'}>
              {result.status === 'valid' ? '✓ Valid Address' : '✗ Invalid Address'}
            </ResultTitle>
            <ResultText>Address: {result.address}</ResultText>
            {result.message && <ResultText>{result.message}</ResultText>}
          </ResultContainer>
        )}
      </Content>
    </Container>
  );
};

export default AddressChecker;
