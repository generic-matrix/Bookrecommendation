import Container from 'react-bootstrap/Container';
import './App.css';
import ReactSearchBox from "react-search-box";
import 'bootstrap/dist/css/bootstrap.min.css';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import React,{useState} from 'react';
import service from './Recommendation';
import Recommendation from './Recommendation';

function App() {

  const [title, setTitle] = useState("");
  const [data, setData] = useState([]);
  const [recommendations,SetRecommendations]=useState(undefined);
  return (
    <div>
      <div className="App">
        <header className="App-header">
          <h1 style={{color:"white"}}>Recommend me the Books</h1>
          <Row className="justify-content-md-center">
          <div style={{padding:40}}>
            <ReactSearchBox
              placeholder="Search For The Books Here"
              value={title}
              inputFontColor="white"
              inputFontSize="40"
              inputBackgroundColor="#282c34"
              onChange={(text)=>{
                setTitle(text)
                service.Autocomplete(text).then((d)=>{
                  setData(d)
                }).catch((error)=>{
                  console.log(error)
                })
              }}
            />
            <div style={{height:40}}></div>
              {
                data.map((d) =>{
                    return <Card onClick={()=>{
                      setData([])
                      const text = d.value;
                      service.Recommendation(text).then((d)=>{
                        if(d!==undefined){
                          if(d.error===null){
                            var arr = []
                            Object.keys(d.data).forEach(function(key) {
                              var value = d.data[key];
                              arr.push(value);
                            });
                            SetRecommendations(arr)
                          }else{
                            SetRecommendations(d.error)
                          }
                        }
                      }).catch((error)=>{
                        console.log(error)
                      })
                    }} bg={'dark'} className="mb-2" style={{ width:'100%',paddingRight:20 }} text={'white'} border="light">
                    <Card.Body>
                      <Card.Text>{d.value}</Card.Text>
                    </Card.Body>
                    </Card> 
                  }
                )
              }
            </div>
          </Row>
          <div style={{height:20}}></div>
          <Container fluid>
            <Col>
            {
              (recommendations!==undefined)?
                (typeof(recommendations)==="object")?
                  recommendations.map((recommendation)=>{
                    return <Card bg={'dark'} className="mb-2" style={{ width:'100%',paddingRight:20 }} text={'white'} border="light">
                      <Card.Body>
                        <Card.Text>{recommendation.title}</Card.Text>
                        <Button variant="primary" onClick={()=>{ window.open("https://amazon.com/"+recommendation.link)}} >Learn More</Button>
                      </Card.Body>
                    </Card> 
                  }):<h1 style={{color:"white"}}>{recommendations}</h1>
                :<></>
            }  
            </Col>
        </Container>
        </header>
      </div>
    </div>
  );
}

export default App;
