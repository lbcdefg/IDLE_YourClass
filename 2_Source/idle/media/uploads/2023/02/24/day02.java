/*
package aa.bb; //패키지 선언

import java.lang.String; //java.lang 패키지는 코어패키지라서 따로 import안해도 됨!
import java.lang.System; //임포트 구문(개수 제한X) 

class A { //클래스선언 
   String name; //멤버변수(속성)
   A(){//생성자
   }
   void m() { //메소드(방법)
   }
}
*/

package aa.bb; // package구문은 1개 이하로만 선언가능, 임포트 구문보다 먼저 나와야함 (순서존재)
import java.lang.String; // 클래스구문보다 항상 임포트 구문이 먼저 나와야함 (순서존재)

class A {      //클래스구문 내에서는 순서존재X
   String name = "홍길동"; //초기화 initializing, 첫번째 들어가는 데이터를 초기값 initial data / 멤버변수는 소괄호 사용하면안됨
   int age = 24;
   A(){
	   System.out.println("A()");
   }
   A(String.name){
	  this.name = name;          // 생성자가 둘 이상일 수 있음, 괄호 내의 파라미터로 구분   작성위치는 상관없음
   }
   void go() {
	   System.out.println("간다");   //m()대신 간다를 입력하면 최종적으로 홍길동이 간다가 나옴!
   }
   void eat() {
	   System.out.println("먹는다");   
   }
}

class Auser{
   public static void main(String args[]){
      A a1 = new A(); //객체1 생성, 생성자메서드 오버로딩, 생성자 호출시에는 반드시 new구문사용
	  System.out.print("나이가 "+a1.age+"인 " + a1.name+"이 ");
	  a1.eat(); //사용

	  A a2 = new A(); //객체2 생성
	  System.out.print("나이가 "+ a2.age + "인 "+a2.name + "이 ");
	  a2.go(); //사용
   }
}
